import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from eval.config import load_json_config, resolve_paths, ensure_output_dirs, require
from eval.w2_reasoning_data import build_reasoning_prompt, read_reasoning_samples
from eval.constants import ENERGY_BATCH_COLUMNS, NA, W2_RAW_COLUMNS
from eval.energy import (
    energy_settings_from_config,
    make_energy_batch_row,
    new_energy_batch_id,
    read_battery,
)
from eval.qnn_pte_runner import QnnPteRunSpec, run_qnn_pte
from eval.tokenizer_utils import resolve_run_max_seq_len
from eval.metrics import now_iso, fmt, to_float_or_none
from eval.parsers import parse_runner_log, read_generation_text, estimate_tpot_ms
from eval.w2_answer_parser import (
    answers_equal,
    parse_final_answer,
    parse_gold_answer,
)
from eval.csv_utils import append_csv
from eval.summarize import summarize_thermal, summarize_w2
from eval.thermal import (
    ThermalReading,
    read_thermal,
    thermal_pair_fields,
    thermal_pair_notes,
    thermal_settings_from_config,
    wait_for_skin_baseline,
)
from eval.failure_report import write_w2_failure_cases
from eval.budget import (
    PHYSICAL_BUDGET_MODE,
    SIMULATED_TRUNCATION_BUDGET_MODE,
    build_budget_view,
    physical_budgets,
    resolve_budget_execution_mode,
)


CONFIG_PATH = SCRIPT_DIR / "run_w2_reasoning_config.json"

def is_expected_seq_len_stop(log_error_type: str, actual_output_tokens: Any, budget: int) -> bool:
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

def classify_w2_error(base: dict[str, Any], deadline_ms: int) -> str:
    runtime_error = base.get("base_error_type", "none")
    if runtime_error != "none" or base.get("returncode") != 0:
        return runtime_error if runtime_error != "none" else "runtime_error"
    if base.get("answer") == NA:
        return "parse_error"
    if not bool(base.get("answer_correct")):
        return "wrong_answer"
    e2e = to_float_or_none(base.get("e2e_latency_ms"))
    if e2e is None:
        return "latency_missing"
    if e2e > deadline_ms:
        return "deadline_miss"
    return "none"

def make_base_row(
    *,
    cfg: dict[str, Any],
    sample: dict[str, Any],
    logical_run_id: str,
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
    returncode: int,
    answer: Any,
    answer_parse_method: str,
    gold_answer: Any,
    gold_parse_method: str,
    answer_correct: bool,
    generated_text_source: str,
    budget_execution_mode: str,
    energy_batch_id: str,
    source_physical_budget: int,
    source_physical_max_seq_len: int,
    start_thermal: ThermalReading,
    end_thermal: ThermalReading,
    common_skin_baseline_c: float | None,
) -> dict[str, Any]:
    runtime = cfg["runtime"]
    runner_cfg = cfg["runner"]

    prompt_tokens = log_metrics.get("prompt_tokens", NA)
    if prompt_tokens == NA and estimated_prompt_tokens != NA:
        prompt_tokens = estimated_prompt_tokens

    actual_output_tokens = log_metrics.get("actual_output_tokens", NA)
    decode_latency_ms = log_metrics.get("decode_latency_ms", NA)
    tpot_ms = estimate_tpot_ms(decode_latency_ms, actual_output_tokens)

    log_error_type = log_metrics.get("error_type", "none")
    stopped_at_budget = is_expected_seq_len_stop(
        log_error_type=log_error_type,
        actual_output_tokens=actual_output_tokens,
        budget=budget,
    )
    runtime_error_type = clean_runtime_error_type(log_error_type, stopped_at_budget)

    notes = [
        # f"logical_run_id={logical_run_id}",
        # f"physical_run_id={physical_run_id}",
        # f"prompt={json.dumps(build_reasoning_prompt(sample, cfg['experiment']['prompt_template']), ensure_ascii=False)}",
        # f"difficulty={sample.get('difficulty', NA)}",
        # f"max_seq_len={max_seq_len}",
        # f"estimated_prompt_tokens={estimated_prompt_tokens}",
        # f"dynamic_max_seq_len={cfg['experiment'].get('dynamic_max_seq_len', True)}",
        # f"budget_execution_mode={budget_execution_mode}",
        # f"energy_batch_id={energy_batch_id}",
        # f"source_physical_budget={source_physical_budget}",
        # f"source_physical_max_seq_len={source_physical_max_seq_len}",
        # f"prefill_ar_len={runner_cfg['prefill_ar_len']}",
        # f"temperature={runner_cfg['temperature']}",
        # f"metrics_source={log_metrics.get('metrics_source', NA)}",
        # f"generated_text_source={generated_text_source}",
        # f"answer_parse_method={answer_parse_method}",
        # f"gold_parse_method={gold_parse_method}",
        # f"stopped_at_budget={stopped_at_budget}",
    ]
    if returncode != 0:
        notes.append(f"returncode={returncode}")
    notes.extend(
        thermal_pair_notes(start_thermal, end_thermal, common_skin_baseline_c)
    )

    return {
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
        "ttft_ms": fmt(log_metrics.get("ttft_ms", NA)),
        "decode_latency_ms": fmt(decode_latency_ms),
        "tpot_ms": tpot_ms,
        "e2e_latency_ms": fmt(log_metrics.get("e2e_latency_ms", NA)),
        "energy_batch_id": energy_batch_id,
        "energy_j": NA,
        **thermal_pair_fields(start_thermal, end_thermal),
        "base_error_type": runtime_error_type,
        "notes": ";".join(notes),
        "answer": answer,
        "gold_answer": gold_answer,
        "answer_correct": answer_correct,
        "reasoning_budget_tokens": budget,
        "output_truncated": fmt(stopped_at_budget),
        "energy_per_correct_answer_j": NA,
        "returncode": returncode,
        "logical_run_id": logical_run_id,
    }

def make_deadline_row(base: dict[str, Any], deadline_ms: int) -> dict[str, Any]:
    row = dict(base)
    row.pop("returncode", None)
    row.pop("base_error_type", None)
    logical_run_id = str(row.pop("logical_run_id"))

    e2e = to_float_or_none(base.get("e2e_latency_ms"))
    answer_correct = bool(base.get("answer_correct"))
    runtime_ok = base.get("base_error_type") == "none" and base.get("returncode") == 0
    correct_under_deadline = runtime_ok and answer_correct and e2e is not None and e2e <= deadline_ms

    row["run_id"] = f"{logical_run_id}_d{deadline_ms}"
    row["deadline_ms"] = deadline_ms
    row["answer_correct"] = fmt(answer_correct)
    row["correct_under_deadline"] = fmt(correct_under_deadline)
    row["task_success"] = fmt(correct_under_deadline)
    row["progress_satisfied"] = fmt(correct_under_deadline)
    row["error_type"] = classify_w2_error(base, deadline_ms)
    return row

def main():
    # 读取并确认输出路径
    cfg = load_json_config(CONFIG_PATH)
    paths = resolve_paths(cfg, CONFIG_PATH)
    ensure_output_dirs(paths)

    # 读取推理样本
    samples = read_reasoning_samples(paths.samples_jsonl)

    # 读取实验、运行时和运行器配置
    experiment = require(cfg, "experiment")
    runtime = require(cfg, "runtime")
    runner_cfg = require(cfg, "runner")

    budgets = [int(x) for x in require(experiment, "reasoning_budgets")]
    budget_execution_mode = resolve_budget_execution_mode(experiment)
    budgets_to_run = physical_budgets(budgets, budget_execution_mode)
    deadlines_ms = [int(x) for x in require(experiment, "deadlines_ms")]
    repeats = int(require(experiment, "repeats"))
    performance_configs = require(experiment, "performance_configs")
    prompt_template = str(require(experiment, "prompt_template"))
    dynamic_max_seq_len = bool(experiment.get("dynamic_max_seq_len", True))
    max_seq_len_cap = int(experiment.get("max_seq_len_cap", runner_cfg.get("max_seq_len", 1024)))
    thermal_settings = thermal_settings_from_config(cfg)
    energy_settings = energy_settings_from_config(cfg)
    common_skin_baseline_c = thermal_settings.baseline_temp_c
    thermal_group_by_column = (
        "reasoning_budget_tokens"
        if budget_execution_mode == PHYSICAL_BUDGET_MODE
        else None
    )

    # 主循环
    for perf in performance_configs:
        perf_name = str(require(perf, "name"))
        htp_mode = perf.get("htp_performance_mode")
        htp_mode = int(htp_mode) if htp_mode is not None else None
        htp_mode_name = str(perf.get("htp_performance_mode_name", NA))
        for physical_budget in budgets_to_run:
            if thermal_settings.enabled:
                common_skin_baseline_c = wait_for_skin_baseline(
                    device=str(require(runtime, "device")),
                    settings=thermal_settings,
                    performance_mode=f"{perf_name}/budget{physical_budget}",
                    target_baseline_c=common_skin_baseline_c,
                )

            energy_batch_id = (
                new_energy_batch_id(
                    cfg["task_group"], perf_name, physical_budget
                )
                if energy_settings.enabled
                else NA
            )
            energy_start = read_battery(
                str(require(runtime, "device")), energy_settings
            )
            batch_physical_runs = 0
            if energy_settings.enabled:
                print(
                    f"[energy] started {energy_batch_id}: "
                    f"counter={energy_start.counter_uah} uAh "
                    f"voltage={energy_start.voltage_mv} mV"
                )

            for sample in samples:
                prompt = build_reasoning_prompt(sample, prompt_template)
                for repeat_id in range(1, repeats + 1):
                    physical_run_id = (
                        f"{sample['sample_id']}_{perf_name}_b{physical_budget}_r{repeat_id}"
                    )
                    log_path = paths.raw_log_dir / f"{physical_run_id}.log"

                    # 解析最大序列长度和提示词令牌数
                    max_seq_len, estimated_prompt_tokens = resolve_run_max_seq_len(
                        runner_cfg=runner_cfg,
                        paths=paths,
                        prompt=prompt,
                        budget=physical_budget,
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

                    # 解析输出日志
                    log_metrics = parse_runner_log(log_path)

                    # 解析标准答案
                    generated_text, generated_text_source = read_generation_text(
                        run_result.token_timestamps_path,
                        run_result.output_text_path,
                    )
                    parsed_gold = parse_gold_answer(sample["gold_answer"])
                    gold_answer = parsed_gold.answer

                    # 是否启用逻辑budgets
                    logical_budgets = (
                        budgets
                        if budget_execution_mode == SIMULATED_TRUNCATION_BUDGET_MODE
                        else [physical_budget]
                    )

                    # 针对不同的budget循环（可能是逻辑/物理）
                    for budget in logical_budgets:
                        logical_run_id = (
                            f"{sample['sample_id']}_{perf_name}_b{budget}_r{repeat_id}"
                        )
                        logical_text = generated_text
                        logical_text_source = generated_text_source
                        logical_metrics = dict(log_metrics)
                        logical_max_seq_len = max_seq_len

                        # 逻辑budget模式下，指标需要变化
                        if budget_execution_mode == SIMULATED_TRUNCATION_BUDGET_MODE:
                            budget_view = build_budget_view(
                                run_result.token_timestamps_path,
                                budget,
                            )
                            logical_text = budget_view.text
                            logical_text_source = "token_timestamps_simulated_budget"
                            if dynamic_max_seq_len and estimated_prompt_tokens != NA:
                                logical_max_seq_len = int(estimated_prompt_tokens) + budget

                            if budget_view.truncated:
                                logical_metrics["actual_output_tokens"] = max(
                                    0, budget_view.output_timestamp_count - 1
                                )
                                logical_metrics["e2e_latency_ms"] = (
                                    budget_view.completion_latency_ms
                                )
                                ttft_ms = to_float_or_none(logical_metrics.get("ttft_ms"))
                                logical_metrics["decode_latency_ms"] = (
                                    max(0.0, budget_view.completion_latency_ms - ttft_ms)
                                    if ttft_ms is not None
                                    else NA
                                )
                                errors = [
                                    error
                                    for error in str(
                                        logical_metrics.get("error_type", "none")
                                    ).split(";")
                                    if error and error != "none"
                                ]
                                errors.extend(["seq_len_limit", "no_eos"])
                                logical_metrics["error_type"] = ";".join(
                                    dict.fromkeys(errors)
                                )
                            logical_metrics["metrics_source"] = (
                                f"{log_metrics.get('metrics_source', NA)}_simulated_budget"
                            )

                        parsed_answer = parse_final_answer(logical_text)
                        answer_correct = answers_equal(parsed_answer.answer, gold_answer)

                        # 输出日志行
                        base = make_base_row(
                            cfg=cfg,
                            sample=sample,
                            logical_run_id=logical_run_id,
                            physical_run_id=physical_run_id,
                            start_time=start_time,
                            end_time=end_time,
                            perf_name=perf_name,
                            htp_mode=htp_mode,
                            htp_mode_name=htp_mode_name,
                            budget=budget,
                            repeat_id=repeat_id,
                            max_seq_len=logical_max_seq_len,
                            estimated_prompt_tokens=estimated_prompt_tokens,
                            log_metrics=logical_metrics,
                            returncode=returncode,
                            answer=parsed_answer.answer,
                            answer_parse_method=parsed_answer.method,
                            gold_answer=gold_answer,
                            gold_parse_method=parsed_gold.method,
                            answer_correct=answer_correct,
                            generated_text_source=logical_text_source,
                            budget_execution_mode=budget_execution_mode,
                            energy_batch_id=energy_batch_id,
                            source_physical_budget=physical_budget,
                            source_physical_max_seq_len=max_seq_len,
                            start_thermal=start_thermal,
                            end_thermal=end_thermal,
                            common_skin_baseline_c=common_skin_baseline_c,
                        )

                    # 每一个deadline_ms都生成一行日志
                        for deadline_ms in deadlines_ms:
                            row = make_deadline_row(base, deadline_ms)
                            append_csv(paths.raw_log_csv, row, W2_RAW_COLUMNS)

                    summarize_w2(
                        paths.raw_log_csv,
                        paths.summary_csv,
                        paths.energy_batch_csv,
                    )
                    summarize_thermal(
                        paths.raw_log_csv,
                        paths.thermal_summary_csv,
                        group_by_column=thermal_group_by_column,
                    )
                    write_w2_failure_cases(paths.raw_log_csv, paths.failure_cases_md)

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
                    physical_budget_tokens=physical_budget,
                    budget_execution_mode=budget_execution_mode,
                    num_physical_runs=batch_physical_runs,
                    start=energy_start,
                    end=energy_end,
                )
                append_csv(
                    paths.energy_batch_csv, energy_row, ENERGY_BATCH_COLUMNS
                )
                summarize_w2(
                    paths.raw_log_csv,
                    paths.summary_csv,
                    paths.energy_batch_csv,
                )
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
