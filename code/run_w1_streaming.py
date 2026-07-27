import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from eval.config import ensure_output_dirs, load_json_config, require, resolve_paths
from eval.constants import ENERGY_BATCH_COLUMNS, NA, W1_RAW_COLUMNS
from eval.csv_utils import append_csv
from eval.energy import (
    energy_settings_from_config,
    make_energy_batch_row,
    new_energy_batch_id,
    read_battery,
)
from eval.failure_report import write_w1_failure_cases
from eval.metrics import fmt, now_iso, to_float_or_none
from eval.parsers import estimate_tpot_ms, parse_runner_log
from eval.qnn_pte_runner import QnnPteRunSpec, run_qnn_pte
from eval.summarize import summarize_thermal, summarize_w1
from eval.thermal import (
    ThermalReading,
    read_thermal,
    thermal_pair_fields,
    thermal_pair_notes,
    thermal_settings_from_config,
    wait_for_skin_baseline,
)
from eval.tokenizer_utils import resolve_run_max_seq_len
from eval.w1_streaming_data import build_streaming_prompt, read_streaming_samples
from eval.w1_token_timing import parse_w1_token_timestamps
from eval.budget import resolve_budget_execution_mode


CONFIG_PATH = SCRIPT_DIR / "run_w1_streaming_config.json"


def is_expected_seq_len_stop(
    log_error_type: str,
    actual_output_tokens: Any,
    budget: int,
) -> bool:
    toks = to_float_or_none(actual_output_tokens)
    if toks is None:
        return False
    reached_budget = toks in {float(budget), float(budget - 1)}
    errors = set(log_error_type.split(";"))
    return reached_budget and {"seq_len_limit", "no_eos"}.issubset(errors)


def clean_runtime_error_type(log_error_type: str, stopped_at_budget: bool) -> str:
    errors = [e for e in log_error_type.split(";") if e]
    if stopped_at_budget:
        errors = [e for e in errors if e not in {"seq_len_limit", "no_eos"}]
    return ";".join(errors) if errors else "none"


def classify_w1_error(base: dict[str, Any]) -> str:
    runtime_error = str(base.get("base_error_type", "none"))
    if runtime_error != "none" or base.get("returncode") != 0:
        return runtime_error if runtime_error != "none" else "runtime_error"
    actual_tokens = to_float_or_none(base.get("actual_output_tokens"))
    if actual_tokens is None or actual_tokens <= 0:
        return "missing_output"
    if to_float_or_none(base.get("tbt_p95_ms")) is None:
        return "token_timing_missing"
    return "none"


def make_row(
    *,
    cfg: dict[str, Any],
    sample: dict[str, Any],
    physical_run_id: str,
    start_time: str,
    end_time: str,
    perf_name: str,
    htp_mode: int | None,
    htp_mode_name: str,
    budget: int,
    repeat_id: int,
    max_seq_len: int,
    estimated_prompt_tokens: Any,
    log_metrics: dict[str, Any],
    token_timing: dict[str, Any],
    returncode: int,
    budget_execution_mode: str,
    energy_batch_id: str,
    start_thermal: ThermalReading,
    end_thermal: ThermalReading,
    common_skin_baseline_c: float | None,
) -> dict[str, Any]:
    runtime = cfg["runtime"]
    runner_cfg = cfg["runner"]
    experiment = cfg["experiment"]

    prompt_tokens = log_metrics.get("prompt_tokens", NA)
    if prompt_tokens == NA and estimated_prompt_tokens != NA:
        prompt_tokens = estimated_prompt_tokens

    actual_output_tokens = token_timing.get("output_token_count", NA)
    actual_output_tokens_source = "token_timestamps"
    if actual_output_tokens == NA:
        actual_output_tokens = log_metrics.get("actual_output_tokens", NA)
        actual_output_tokens_source = "runner_log"

    decode_latency_ms = log_metrics.get("decode_latency_ms", NA)
    tpot_ms = estimate_tpot_ms(decode_latency_ms, actual_output_tokens)

    ttft_ms = log_metrics.get("ttft_ms", NA)
    ttft_source = "runner_log"
    if ttft_ms == NA:
        ttft_ms = token_timing.get("ttft_from_token_timestamps_ms", NA)
        ttft_source = "token_timestamps"

    visible_tps = token_timing.get("visible_tokens_per_second", NA)
    visible_tps_source = "token_timestamps"
    if visible_tps == NA:
        visible_tps = log_metrics.get("visible_tokens_per_second", NA)
        visible_tps_source = "runner_log"

    log_error_type = log_metrics.get("error_type", "none")
    stopped_at_budget = is_expected_seq_len_stop(
        log_error_type=log_error_type,
        actual_output_tokens=actual_output_tokens,
        budget=budget,
    )
    runtime_error_type = clean_runtime_error_type(log_error_type, stopped_at_budget)

    p95_tbt = to_float_or_none(token_timing.get("tbt_p95_ms"))
    average_reading_ms = float(experiment["reading_thresholds_ms"]["average_reading"])
    progress_satisfied: Any = NA if p95_tbt is None else p95_tbt <= average_reading_ms

    prompt = build_streaming_prompt(sample, experiment["prompt_template"])
    notes = [
        # f"physical_run_id={physical_run_id}",
        # f"prompt={json.dumps(prompt, ensure_ascii=False)}",
        # f"difficulty={sample.get('difficulty', NA)}",
        # f"max_seq_len={max_seq_len}",
        # f"estimated_prompt_tokens={estimated_prompt_tokens}",
        # f"dynamic_max_seq_len={experiment.get('dynamic_max_seq_len', True)}",
        # f"budget_execution_mode={budget_execution_mode}",
        # f"energy_batch_id={energy_batch_id}",
        # f"prefill_ar_len={runner_cfg['prefill_ar_len']}",
        # f"temperature={runner_cfg['temperature']}",
        # f"metrics_source={log_metrics.get('metrics_source', NA)}",
        # f"actual_output_tokens_source={actual_output_tokens_source}",
        # f"ttft_source={ttft_source}",
        # f"visible_tokens_per_second_source={visible_tps_source}",
        # f"stopped_at_budget={stopped_at_budget}",
        # f"average_reading_threshold_ms={average_reading_ms}",
        # token_timing["notes_token_timing"],
    ]
    if returncode != 0:
        notes.append(f"returncode={returncode}")
    notes.extend(
        thermal_pair_notes(start_thermal, end_thermal, common_skin_baseline_c)
    )

    row = {
        "run_id": physical_run_id,
        "timestamp_start": start_time,
        "timestamp_end": end_time,
        "assignee": cfg["assignee"],
        "task_group": cfg["task_group"],
        "device_id": runtime["device"],
        "runtime": runtime["name"],
        "model": runtime["model_name"],
        "quantization": runtime["quantization"],
        "backend": runtime["backend"],
        "performance_mode": perf_name,
        "htp_performance_mode": htp_mode if htp_mode is not None else NA,
        "htp_performance_mode_name": htp_mode_name,
        "strategy": (
            f"{runner_cfg['model_mode']}_prefill_ar{runner_cfg['prefill_ar_len']}_"
            f"seq{max_seq_len}_budget{budget}_temp{runner_cfg['temperature']}"
        ),
        "dataset": sample.get("dataset", NA),
        "sample_id": sample["sample_id"],
        "repeat_id": repeat_id,
        "prompt_tokens": prompt_tokens,
        "target_output_tokens": budget,
        "actual_output_tokens": actual_output_tokens,
        "ttft_ms": fmt(ttft_ms),
        "decode_latency_ms": fmt(decode_latency_ms),
        "tpot_ms": tpot_ms,
        "e2e_latency_ms": fmt(log_metrics.get("e2e_latency_ms", NA)),
        "energy_batch_id": energy_batch_id,
        "energy_j": NA,
        **thermal_pair_fields(start_thermal, end_thermal),
        "deadline_ms": NA,
        "progress_satisfied": fmt(progress_satisfied),
        "base_error_type": runtime_error_type,
        "returncode": returncode,
        "notes": ";".join(notes),
        "tbt_p50_ms": token_timing.get("tbt_p50_ms", NA),
        "tbt_p95_ms": token_timing.get("tbt_p95_ms", NA),
        "stall_ratio": token_timing.get("stall_ratio", NA),
        "visible_tokens_per_second": visible_tps,
    }

    error_type = classify_w1_error(row)
    row["error_type"] = error_type
    row["task_success"] = fmt(error_type == "none")
    row.pop("base_error_type", None)
    row.pop("returncode", None)
    return row


def main() -> None:
    # 读取并确认输出路径
    cfg = load_json_config(CONFIG_PATH)
    paths = resolve_paths(cfg, CONFIG_PATH)
    ensure_output_dirs(paths)

    # 读取流式问答样本
    samples = read_streaming_samples(paths.samples_jsonl)

    # 读取实验、运行时和运行器配置
    experiment = require(cfg, "experiment")
    runtime = require(cfg, "runtime")
    runner_cfg = require(cfg, "runner")

    budget = int(require(experiment, "target_output_tokens"))
    budget_execution_mode = resolve_budget_execution_mode(experiment)
    repeats = int(require(experiment, "repeats"))
    performance_configs = require(experiment, "performance_configs")
    prompt_template = str(require(experiment, "prompt_template"))
    stall_threshold_ms = float(require(experiment, "stall_threshold_ms"))
    reading_thresholds_ms = require(experiment, "reading_thresholds_ms")
    average_reading_ms = float(require(reading_thresholds_ms, "average_reading"))
    tight_reading_ms = float(require(reading_thresholds_ms, "tight_reading"))
    high_end_chatbot_ms = float(require(reading_thresholds_ms, "high_end_chatbot"))
    dynamic_max_seq_len = bool(experiment.get("dynamic_max_seq_len", True))
    max_seq_len_cap = int(experiment.get("max_seq_len_cap", runner_cfg.get("max_seq_len", 1024)))
    thermal_settings = thermal_settings_from_config(cfg)
    energy_settings = energy_settings_from_config(cfg)
    common_skin_baseline_c = thermal_settings.baseline_temp_c

    # 主循环
    for perf in performance_configs:
        perf_name = str(require(perf, "name"))
        htp_mode = perf.get("htp_performance_mode")
        htp_mode = int(htp_mode) if htp_mode is not None else None
        htp_mode_name = str(perf.get("htp_performance_mode_name", NA))
        if thermal_settings.enabled:
            common_skin_baseline_c = wait_for_skin_baseline(
                device=str(require(runtime, "device")),
                settings=thermal_settings,
                performance_mode=perf_name,
                target_baseline_c=common_skin_baseline_c,
            )

        energy_batch_id = (
            new_energy_batch_id(cfg["task_group"], perf_name, budget)
            if energy_settings.enabled
            else NA
        )
        energy_start = read_battery(str(require(runtime, "device")), energy_settings)
        batch_physical_runs = 0
        if energy_settings.enabled:
            print(
                f"[energy] started {energy_batch_id}: "
                f"counter={energy_start.counter_uah} uAh "
                f"voltage={energy_start.voltage_mv} mV"
            )

        for sample in samples:
            prompt = build_streaming_prompt(sample, prompt_template)

            for repeat_id in range(1, repeats + 1):
                physical_run_id = f"{sample['sample_id']}_{perf_name}_b{budget}_r{repeat_id}"
                log_path = paths.raw_log_dir / f"{physical_run_id}.log"

                # 解析最大序列长度和提示词令牌数
                max_seq_len, estimated_prompt_tokens = resolve_run_max_seq_len(
                    runner_cfg=runner_cfg,
                    paths=paths,
                    prompt=prompt,
                    budget=budget,
                    dynamic_max_seq_len=dynamic_max_seq_len,
                    max_seq_len_cap=max_seq_len_cap,
                )

                output_dir = paths.runner_output_dir / physical_run_id
                run_spec = QnnPteRunSpec(
                    device=str(require(runtime, "device")),
                    artifact=paths.pre_gen_pte,
                    decoder_model=str(require(runner_cfg, "decoder_model")),
                    model_mode=str(require(runner_cfg, "model_mode")),
                    prompt=prompt,
                    max_seq_len=max_seq_len,
                    temperature=float(require(runner_cfg, "temperature")),
                    htp_performance_mode=htp_mode if htp_mode is not None else 2,
                    system_prompt=str(runner_cfg.get("system_prompt", "")),
                )

                # 运行设备推理并将终端输出写入raw_runner_logs
                start_thermal = read_thermal(
                    str(require(runtime, "device")), thermal_settings
                )
                start_time = now_iso()
                run_result = run_qnn_pte(
                    run_spec,
                    output_dir=output_dir,
                    log_path=log_path,
                )
                returncode = run_result.returncode
                batch_physical_runs += 1
                end_time = now_iso()
                end_thermal = read_thermal(
                    str(require(runtime, "device")), thermal_settings
                )

                # 解析runner日志和逐token时间戳
                log_metrics = parse_runner_log(log_path)
                token_timing = parse_w1_token_timestamps(
                    run_result.token_timestamps_path,
                    stall_threshold_ms=stall_threshold_ms,
                )

                # 输出日志行
                row = make_row(
                    cfg=cfg,
                    sample=sample,
                    physical_run_id=physical_run_id,
                    start_time=start_time,
                    end_time=end_time,
                    perf_name=perf_name,
                    htp_mode=htp_mode,
                    htp_mode_name=htp_mode_name,
                    budget=budget,
                    repeat_id=repeat_id,
                    max_seq_len=max_seq_len,
                    estimated_prompt_tokens=estimated_prompt_tokens,
                    log_metrics=log_metrics,
                    token_timing=token_timing,
                    returncode=returncode,
                    budget_execution_mode=budget_execution_mode,
                    energy_batch_id=energy_batch_id,
                    start_thermal=start_thermal,
                    end_thermal=end_thermal,
                    common_skin_baseline_c=common_skin_baseline_c,
                )
                append_csv(paths.raw_log_csv, row, W1_RAW_COLUMNS)

                summarize_w1(
                    paths.raw_log_csv,
                    paths.summary_csv,
                    average_reading_ms=average_reading_ms,
                    tight_reading_ms=tight_reading_ms,
                    high_end_chatbot_ms=high_end_chatbot_ms,
                )
                summarize_thermal(paths.raw_log_csv, paths.thermal_summary_csv)
                write_w1_failure_cases(paths.raw_log_csv, paths.failure_cases_md)

                print(f"[saved outputs] {run_result.output_dir}")
                print(f"[saved] {paths.raw_log_csv}")
                print(f"[saved] {paths.summary_csv}")
                print(f"[saved] {paths.thermal_summary_csv}")
                print(f"[saved] {paths.failure_cases_md}")

        if energy_settings.enabled:
            energy_end = read_battery(
                str(require(runtime, "device")), energy_settings
            )
            energy_row = make_energy_batch_row(
                cfg=cfg,
                settings=energy_settings,
                energy_batch_id=energy_batch_id,
                performance_mode=perf_name,
                htp_performance_mode=htp_mode,
                htp_performance_mode_name=htp_mode_name,
                physical_budget_tokens=budget,
                budget_execution_mode=budget_execution_mode,
                num_physical_runs=batch_physical_runs,
                start=energy_start,
                end=energy_end,
            )
            append_csv(paths.energy_batch_csv, energy_row, ENERGY_BATCH_COLUMNS)
            print(
                f"[energy] finished {energy_batch_id}: "
                f"energy={energy_row['gross_energy_j']} J "
                f"ticks={energy_row['counter_ticks']} "
                f"status={energy_row['measurement_status']}"
            )
            print(f"[saved] {paths.energy_batch_csv}")

    print("\nDone.")


if __name__ == "__main__":
    main()
