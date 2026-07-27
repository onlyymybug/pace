import json
from pathlib import Path
from typing import Any

from .constants import NA
from .metrics import fmt, percentile, to_float_or_none


def _empty_timing(reason: str, output_token_count: Any = NA) -> dict[str, Any]:
    return {
        "tbt_p50_ms": NA,
        "tbt_p95_ms": NA,
        "stall_ratio": NA,
        "visible_tokens_per_second": NA,
        "output_token_count": output_token_count,
        "ttft_from_token_timestamps_ms": NA,
        "timing_source": "unavailable",
        "notes_token_timing": reason,
    }


def parse_w1_token_timestamps(
    path: Path,
    stall_threshold_ms: float,
) -> dict[str, Any]:
    if not path.exists():
        return _empty_timing("token_timestamps_missing")

    rows: list[dict[str, Any]] = []
    invalid_json_lines = 0
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                invalid_json_lines += 1
                continue
            if isinstance(row, dict):
                rows.append(row)

    if not rows:
        return _empty_timing("token_timestamps_empty_or_invalid")

    output_rows = [r for r in rows if not bool(r.get("prompt_echo", False))]
    output_token_count = len(output_rows)
    if not output_rows:
        return _empty_timing("no_output_token_timestamps", output_token_count=0)

    absolute_times = [to_float_or_none(r.get("timestamp_ms")) for r in output_rows]
    delta_times = [to_float_or_none(r.get("delta_ms")) for r in output_rows]

    if all(t is not None for t in absolute_times):
        times = [float(t) for t in absolute_times if t is not None]
        timing_source = "timestamp_ms"
    elif all(t is not None for t in delta_times):
        times = [float(t) for t in delta_times if t is not None]
        timing_source = "delta_ms"
    else:
        return _empty_timing(
            "output_token_timestamps_incomplete",
            output_token_count=output_token_count,
        )

    gaps = [times[i] - times[i - 1] for i in range(1, len(times))]
    if any(g < 0 for g in gaps):
        return _empty_timing(
            "output_token_timestamps_not_monotonic",
            output_token_count=output_token_count,
        )

    first_output_delta = to_float_or_none(output_rows[0].get("delta_ms"))
    if first_output_delta is None:
        first_row_timestamp = to_float_or_none(rows[0].get("timestamp_ms"))
        first_output_timestamp = to_float_or_none(output_rows[0].get("timestamp_ms"))
        if first_row_timestamp is not None and first_output_timestamp is not None:
            first_output_delta = first_output_timestamp - first_row_timestamp

    if gaps:
        stall_count = sum(g > stall_threshold_ms for g in gaps)
        stall_ratio = stall_count / len(gaps)
        duration_ms = times[-1] - times[0]
        visible_tps = 1000.0 * len(gaps) / duration_ms if duration_ms > 0 else NA
    else:
        stall_ratio = NA
        visible_tps = NA

    notes = [
        "token_timestamps_ok",
        f"n_output_tokens={output_token_count}",
        f"n_inter_token_gaps={len(gaps)}",
        f"stall_threshold_ms={stall_threshold_ms}",
        f"timing_source={timing_source}",
    ]
    if invalid_json_lines:
        notes.append(f"invalid_json_lines={invalid_json_lines}")

    return {
        "tbt_p50_ms": percentile(gaps, 50),
        "tbt_p95_ms": percentile(gaps, 95),
        "stall_ratio": fmt(stall_ratio, 6),
        "visible_tokens_per_second": fmt(visible_tps),
        "output_token_count": output_token_count,
        "ttft_from_token_timestamps_ms": fmt(first_output_delta),
        "timing_source": timing_source,
        "notes_token_timing": ";".join(notes),
    }
