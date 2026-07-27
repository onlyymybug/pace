from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .constants import (
    NA,
    THERMAL_SUMMARY_COLUMNS,
    W1_SUMMARY_COLUMNS,
    W2_SUMMARY_COLUMNS,
    W3_SUMMARY_COLUMNS,
)
from .csv_utils import read_csv, write_csv
from .metrics import bool_rate, mean, percentile, to_float_or_none, fmt


_RUNTIME_ERROR_TYPES = {
    "missing_output",
    "missing_returncode",
    "no_eos",
    "python_traceback",
    "runtime_error",
    "runtime_error_or_missing_returncode",
    "runtime_error_text",
    "seq_len_limit",
}

_W2_PARSE_ERROR_TRUNCATED = "parse_error_truncated"
_W2_PARSE_ERROR_UNTRUNCATED = "parse_error_untruncated"
_W2_WRONG_ANSWER = "wrong_answer"
_W2_DEADLINE_MISS = "deadline_miss"
_W2_OTHER_ERRORS = "other_errors"


def _physical_run_id(run_id: str) -> str:
    if "_d" in run_id:
        return run_id.rsplit("_d", 1)[0]
    return run_id


def _note_value(row: dict[str, str], key: str) -> str | None:
    prefix = f"{key}="
    for item in row.get("notes", "").split(";"):
        if item.startswith(prefix):
            return item[len(prefix) :]
    return None


def _physical_measurement_key(row: dict[str, str]) -> tuple[str, str, str]:
    physical_run_id = _note_value(row, "physical_run_id")
    if physical_run_id is None:
        physical_run_id = _physical_run_id(row.get("run_id", ""))
    return (
        row.get("device_id", NA),
        row.get("timestamp_start", NA),
        physical_run_id,
    )


def _deduplicate_physical_measurements(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in rows:
        unique.setdefault(_physical_measurement_key(row), row)
    return list(unique.values())


def _paired_delta(row: dict[str, str], start_key: str, end_key: str) -> float | None:
    start = to_float_or_none(row.get(start_key))
    end = to_float_or_none(row.get(end_key))
    if start is None or end is None:
        return None
    return end - start


def _max_observed(rows: list[dict[str, str]], *keys: str) -> Any:
    values = [
        value
        for row in rows
        for key in keys
        if (value := to_float_or_none(row.get(key))) is not None
    ]
    return fmt(max(values)) if values else NA


def _has_runtime_error(row: dict[str, str]) -> bool:
    error_types = {
        error_type
        for error_type in row.get("error_type", "").split(";")
        if error_type
    }
    return bool(error_types & _RUNTIME_ERROR_TYPES)


def _runtime_success(row: dict[str, str]) -> bool:
    return not _has_runtime_error(row)


def _w2_error_bucket(row: dict[str, str]) -> str | None:
    error_type = row.get("error_type", "")
    if error_type == "parse_error":
        if row.get("output_truncated") == "true":
            return _W2_PARSE_ERROR_TRUNCATED
        if row.get("output_truncated") == "false":
            return _W2_PARSE_ERROR_UNTRUNCATED
    elif error_type == "wrong_answer":
        return _W2_WRONG_ANSWER
    elif error_type == "deadline_miss":
        return _W2_DEADLINE_MISS

    if row.get("correct_under_deadline") != "true":
        return _W2_OTHER_ERRORS
    return None


def _tokens_per_second(r: dict[str, str]) -> Any:
    toks = to_float_or_none(r.get("actual_output_tokens"))
    e2e = to_float_or_none(r.get("e2e_latency_ms"))
    if toks is None or e2e is None or e2e <= 0:
        return NA
    return toks / (e2e / 1000.0)


def _legacy_energy_per_correct_answer(rs: list[dict[str, str]]) -> Any:
    energy_vals = [to_float_or_none(r.get("energy_j")) for r in rs]
    if not any(v is not None for v in energy_vals):
        return NA
    total_energy = sum(v for v in energy_vals if v is not None)
    num_correct = sum(r.get("correct_under_deadline") == "true" for r in rs)
    if num_correct <= 0:
        return NA
    return fmt(total_energy / num_correct)


def _batch_energy_per_correct_answer(
    rs: list[dict[str, str]],
    energy_batches: dict[str, dict[str, str]],
    logical_budget: str,
) -> Any:
    matching_batch_ids = {
        row.get("energy_batch_id", "")
        for row in rs
        if row.get("energy_batch_id", "") in energy_batches
        and energy_batches[row["energy_batch_id"]].get("valid_for_reporting") == "true"
        and energy_batches[row["energy_batch_id"]].get("physical_budget_tokens")
        == logical_budget
    }
    if not matching_batch_ids:
        return NA

    batch_energy_values = [
        to_float_or_none(energy_batches[batch_id].get("gross_energy_j"))
        for batch_id in matching_batch_ids
    ]
    if any(value is None for value in batch_energy_values):
        return NA
    total_energy = sum(value for value in batch_energy_values if value is not None)
    correct_physical_runs = {
        _physical_measurement_key(row)
        for row in rs
        if row.get("energy_batch_id", "") in matching_batch_ids
        and row.get("correct_under_deadline") == "true"
    }
    if not correct_physical_runs:
        return NA
    return fmt(total_energy / len(correct_physical_runs))

def _threshold_pass_rate(
    rows: list[dict[str, str]],
    threshold_ms: float,
) -> Any:
    values = [to_float_or_none(r.get("tbt_p95_ms")) for r in rows]
    values = [v for v in values if v is not None]
    if not values:
        return NA
    return fmt(sum(v <= threshold_ms for v in values) / len(values), 6)

def summarize_w1(
    raw_csv: Path,
    summary_csv: Path,
    *,
    average_reading_ms: float,
    tight_reading_ms: float,
    high_end_chatbot_ms: float,
) -> None:
    rows = read_csv(raw_csv)
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)

    for r in rows:
        key = (
            r.get("runtime", NA),
            r.get("model", NA),
            r.get("backend", NA),
            r.get("performance_mode", NA),
            r.get("htp_performance_mode", NA),
            r.get("htp_performance_mode_name", NA),
            r.get("dataset", NA),
            r.get("target_output_tokens", NA),
        )
        groups[key].append(r)

    out_rows: list[dict[str, Any]] = []
    for key, rs in sorted(groups.items()):
        ttft_vals = [to_float_or_none(r.get("ttft_ms")) for r in rs]
        ttft_vals = [v for v in ttft_vals if v is not None]
        e2e_vals = [to_float_or_none(r.get("e2e_latency_ms")) for r in rs]
        e2e_vals = [v for v in e2e_vals if v is not None]
        unique_runs = {r.get("run_id", "") for r in rs}

        out_rows.append(
            {
                "runtime": key[0],
                "model": key[1],
                "backend": key[2],
                "performance_mode": key[3],
                "htp_performance_mode": key[4],
                "htp_performance_mode_name": key[5],
                "dataset": key[6],
                "target_output_tokens": key[7],
                "num_rows": len(rs),
                "num_unique_runs": len(unique_runs),
                "task_success_rate": bool_rate(r.get("task_success") for r in rs),
                "progress_satisfied_rate": bool_rate(r.get("progress_satisfied") for r in rs),
                "ttft_mean_ms": mean(ttft_vals),
                "ttft_p50_ms": percentile(ttft_vals, 50),
                "ttft_p95_ms": percentile(ttft_vals, 95),
                "e2e_mean_ms": mean(e2e_vals),
                "e2e_p50_ms": percentile(e2e_vals, 50),
                "e2e_p95_ms": percentile(e2e_vals, 95),
                "decode_latency_mean_ms": mean(r.get("decode_latency_ms") for r in rs),
                "actual_output_tokens_mean": mean(r.get("actual_output_tokens") for r in rs),
                "visible_tokens_per_second_mean": mean(
                    r.get("visible_tokens_per_second") for r in rs
                ),
                "tbt_p50_mean_ms": mean(r.get("tbt_p50_ms") for r in rs),
                "tbt_p95_mean_ms": mean(r.get("tbt_p95_ms") for r in rs),
                "stall_ratio_mean": mean(r.get("stall_ratio") for r in rs),
                "pass_4_8_tps_rate": _threshold_pass_rate(rs, average_reading_ms),
                "pass_6_tps_rate": _threshold_pass_rate(rs, tight_reading_ms),
                "pass_10_tps_rate": _threshold_pass_rate(rs, high_end_chatbot_ms),
            }
        )

    write_csv(summary_csv, out_rows, W1_SUMMARY_COLUMNS)

def summarize_w2(
    raw_csv: Path,
    summary_csv: Path,
    energy_batch_csv: Path | None = None,
) -> None:
    rows = read_csv(raw_csv)
    energy_batch_rows = read_csv(energy_batch_csv) if energy_batch_csv else []
    energy_batches = {
        row.get("energy_batch_id", ""): row
        for row in energy_batch_rows
        if row.get("energy_batch_id")
    }
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)

    for r in rows:
        key = (
            r.get("runtime", NA),
            r.get("model", NA),
            r.get("backend", NA),
            r.get("performance_mode", NA),
            r.get("htp_performance_mode", NA),
            r.get("htp_performance_mode_name", NA),
            r.get("reasoning_budget_tokens", NA),
            r.get("deadline_ms", NA),
        )
        groups[key].append(r)

    out_rows: list[dict[str, Any]] = []
    for key, rs in sorted(groups.items()):
        e2e_vals = [to_float_or_none(r.get("e2e_latency_ms")) for r in rs]
        e2e_vals = [v for v in e2e_vals if v is not None]
        unique_physical_runs = {
            _physical_run_id(r.get("run_id", "")) for r in rs
        }
        error_counts = Counter(
            bucket
            for row in rs
            if (bucket := _w2_error_bucket(row)) is not None
        )
        out_rows.append(
            {
                "runtime": key[0],
                "model": key[1],
                "backend": key[2],
                "performance_mode": key[3],
                "htp_performance_mode": key[4],
                "htp_performance_mode_name": key[5],
                "reasoning_budget_tokens": key[6],
                "deadline_ms": key[7],
                "num_rows": len(rs),
                "num_unique_runs": len(unique_physical_runs),
                "parse_error_truncated_count": error_counts[
                    _W2_PARSE_ERROR_TRUNCATED
                ],
                "parse_error_untruncated_count": error_counts[
                    _W2_PARSE_ERROR_UNTRUNCATED
                ],
                "wrong_answer_count": error_counts[_W2_WRONG_ANSWER],
                "deadline_miss_count": error_counts[_W2_DEADLINE_MISS],
                "other_errors_count": error_counts[_W2_OTHER_ERRORS],
                "runtime_success_rate": bool_rate(_runtime_success(r) for r in rs),
                "answer_correct_rate": bool_rate(r.get("answer_correct") for r in rs),
                "correct_under_deadline_rate": bool_rate(r.get("correct_under_deadline") for r in rs),
                "e2e_mean_ms": mean(e2e_vals),
                "e2e_p50_ms": percentile(e2e_vals, 50),
                "e2e_p95_ms": percentile(e2e_vals, 95),
                "decode_latency_mean_ms": mean(r.get("decode_latency_ms") for r in rs),
                "actual_output_tokens_mean": mean(r.get("actual_output_tokens") for r in rs),
                "e2e_output_tokens_per_second_mean": mean(
                    _tokens_per_second(r) for r in rs
                ),
                "energy_per_correct_answer_j": (
                    _batch_energy_per_correct_answer(rs, energy_batches, key[6])
                    if energy_batch_csv is not None
                    else _legacy_energy_per_correct_answer(rs)
                ),
            }
        )

    write_csv(summary_csv, out_rows, W2_SUMMARY_COLUMNS)

def summarize_w3(raw_csv: Path, summary_csv: Path) -> None:
    rows = read_csv(raw_csv)
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)

    for r in rows:
        key = (
            r.get("runtime", NA),
            r.get("model", NA),
            r.get("backend", NA),
            r.get("performance_mode", NA),
            r.get("htp_performance_mode", NA),
            r.get("htp_performance_mode_name", NA),
            r.get("dataset", NA),
            r.get("action_budget_tokens", NA),
            r.get("deadline_ms", NA),
        )
        groups[key].append(r)

    out_rows: list[dict[str, Any]] = []
    for key, rs in sorted(groups.items()):
        e2e_vals = [to_float_or_none(r.get("e2e_latency_ms")) for r in rs]
        e2e_vals = [v for v in e2e_vals if v is not None]
        valid_time_vals = [
            to_float_or_none(r.get("time_to_valid_action_ms"))
            for r in rs
            if r.get("action_valid") == "true"
        ]
        valid_time_vals = [v for v in valid_time_vals if v is not None]
        unique_physical_runs = {_physical_run_id(r.get("run_id", "")) for r in rs}

        out_rows.append(
            {
                "runtime": key[0],
                "model": key[1],
                "backend": key[2],
                "performance_mode": key[3],
                "htp_performance_mode": key[4],
                "htp_performance_mode_name": key[5],
                "dataset": key[6],
                "action_budget_tokens": key[7],
                "deadline_ms": key[8],
                "num_rows": len(rs),
                "num_unique_runs": len(unique_physical_runs),
                "runtime_success_rate": bool_rate(_runtime_success(r) for r in rs),
                "action_valid_rate": bool_rate(r.get("action_valid") for r in rs),
                "action_correct_rate": bool_rate(r.get("action_correct") for r in rs),
                "valid_under_deadline_rate": bool_rate(r.get("valid_under_deadline") for r in rs),
                "correct_under_deadline_rate": bool_rate(r.get("correct_under_deadline") for r in rs),
                "invalid_action_rate": mean(r.get("invalid_action_rate") for r in rs),
                "time_to_valid_action_mean_ms": mean(valid_time_vals),
                "time_to_valid_action_p50_ms": percentile(valid_time_vals, 50),
                "time_to_valid_action_p95_ms": percentile(valid_time_vals, 95),
                "e2e_mean_ms": mean(e2e_vals),
                "e2e_p50_ms": percentile(e2e_vals, 50),
                "e2e_p95_ms": percentile(e2e_vals, 95),
                "decode_latency_mean_ms": mean(r.get("decode_latency_ms") for r in rs),
                "actual_output_tokens_mean": mean(r.get("actual_output_tokens") for r in rs),
                "e2e_output_tokens_per_second_mean": mean(
                    _tokens_per_second(r) for r in rs
                ),
                "parse_error_rate": bool_rate(r.get("error_type") == "parse_error" for r in rs),
                "schema_error_rate": bool_rate(r.get("error_type") == "schema_error" for r in rs),
                "wrong_action_type_rate": bool_rate(r.get("error_type") == "wrong_action_type" for r in rs),
                "wrong_argument_rate": bool_rate(r.get("error_type") == "wrong_argument" for r in rs),
                "deadline_miss_rate": bool_rate(r.get("error_type") == "deadline_miss" for r in rs),
                "runtime_error_rate": bool_rate(_has_runtime_error(r) for r in rs),
            }
        )

    write_csv(summary_csv, out_rows, W3_SUMMARY_COLUMNS)


def summarize_thermal(
    raw_csv: Path,
    summary_csv: Path,
    *,
    group_by_column: str | None = None,
) -> None:
    rows = read_csv(raw_csv)
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key: tuple[str, ...] = (
            row.get("task_group", NA),
            row.get("runtime", NA),
            row.get("model", NA),
            row.get("backend", NA),
            row.get("performance_mode", NA),
            row.get("htp_performance_mode", NA),
            row.get("htp_performance_mode_name", NA),
        )
        if group_by_column is not None:
            key += (row.get(group_by_column, NA),)
        groups[key].append(row)

    out_rows: list[dict[str, Any]] = []
    for key, group_rows in sorted(groups.items()):
        physical_rows = _deduplicate_physical_measurements(group_rows)
        measured_rows = [
            row
            for row in physical_rows
            if to_float_or_none(row.get("start_temp_c")) is not None
            and to_float_or_none(row.get("end_temp_c")) is not None
        ]
        summary_row = {
            "task_group": key[0],
            "runtime": key[1],
            "model": key[2],
            "backend": key[3],
            "performance_mode": key[4],
            "htp_performance_mode": key[5],
            "htp_performance_mode_name": key[6],
            "num_rows": len(group_rows),
            "num_unique_physical_runs": len(physical_rows),
            "num_measured_physical_runs": len(measured_rows),
            "start_temp_mean_c": mean(row.get("start_temp_c") for row in physical_rows),
            "end_temp_mean_c": mean(row.get("end_temp_c") for row in physical_rows),
            "skin_temp_delta_mean_c": mean(
                _paired_delta(row, "start_temp_c", "end_temp_c")
                for row in physical_rows
            ),
            "max_observed_skin_temp_c": _max_observed(
                physical_rows, "start_temp_c", "end_temp_c"
            ),
            "start_npu_temp_mean_c": mean(
                row.get("start_npu_temp_c") for row in physical_rows
            ),
            "end_npu_temp_mean_c": mean(
                row.get("end_npu_temp_c") for row in physical_rows
            ),
            "npu_temp_delta_mean_c": mean(
                _paired_delta(row, "start_npu_temp_c", "end_npu_temp_c")
                for row in physical_rows
            ),
            "max_observed_npu_temp_c": _max_observed(
                physical_rows, "start_npu_temp_c", "end_npu_temp_c"
            ),
            "max_thermal_status": _max_observed(physical_rows, "thermal_status"),
        }
        if group_by_column is not None:
            summary_row[group_by_column] = key[7]
        out_rows.append(summary_row)

    columns = list(THERMAL_SUMMARY_COLUMNS)
    if group_by_column is not None:
        columns.insert(7, group_by_column)
    write_csv(summary_csv, out_rows, columns)
