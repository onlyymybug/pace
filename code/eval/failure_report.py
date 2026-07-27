from __future__ import annotations

from pathlib import Path

from .csv_utils import read_csv

def write_w1_failure_cases(raw_csv: Path, failure_cases_md: Path, max_cases: int = 200) -> None:
    rows = read_csv(raw_csv)
    bad = [
        r
        for r in rows
        if r.get("task_success") != "true" or r.get("progress_satisfied") != "true"
    ]

    with failure_cases_md.open("w", encoding="utf-8") as f:
        f.write("# W1 failure cases\n\n")
        f.write(
            "A row is listed when the run failed to produce trustworthy token timing "
            "or when `p95 TBT` did not satisfy the average-reading threshold. "
            "The per-run outputs are archived under `runner_outputs/`.\n\n"
        )
        if not bad:
            f.write("No failure cases.\n")
            return

        for i, r in enumerate(bad[:max_cases], start=1):
            f.write(f"## {i}. {r.get('run_id')}\n\n")
            f.write(f"- sample_id: `{r.get('sample_id')}`\n")
            f.write(f"- performance_mode: `{r.get('performance_mode')}`\n")
            f.write(f"- target_output_tokens: `{r.get('target_output_tokens')}`\n")
            f.write(f"- ttft_ms: `{r.get('ttft_ms')}`\n")
            f.write(f"- tbt_p95_ms: `{r.get('tbt_p95_ms')}`\n")
            f.write(f"- stall_ratio: `{r.get('stall_ratio')}`\n")
            f.write(
                f"- visible_tokens_per_second: `{r.get('visible_tokens_per_second')}`\n"
            )
            f.write(f"- task_success: `{r.get('task_success')}`\n")
            f.write(f"- progress_satisfied: `{r.get('progress_satisfied')}`\n")
            f.write(f"- error_type: `{r.get('error_type')}`\n")
            f.write(f"- notes: `{r.get('notes', '')[:800]}`\n\n")

def write_w2_failure_cases(raw_csv: Path, failure_cases_md: Path, max_cases: int = 200) -> None:
    rows = read_csv(raw_csv)
    bad = [
        r
        for r in rows
        if r.get("correct_under_deadline") != "true"
    ]

    with failure_cases_md.open("w", encoding="utf-8") as f:
        f.write("# W2 failure cases\n\n")
        f.write(
            "A row is treated as a failure when `correct_under_deadline != true`. "
            "The generated text is archived under `runner_outputs/` for each physical run.\n\n"
        )
        if not bad:
            f.write("No failure cases.\n")
            return

        for i, r in enumerate(bad[:max_cases], start=1):
            f.write(f"## {i}. {r.get('run_id')}\n\n")
            f.write(f"- sample_id: `{r.get('sample_id')}`\n")
            f.write(f"- performance_mode: `{r.get('performance_mode')}`\n")
            f.write(f"- budget: `{r.get('reasoning_budget_tokens')}`\n")
            f.write(f"- deadline_ms: `{r.get('deadline_ms')}`\n")
            f.write(f"- e2e_latency_ms: `{r.get('e2e_latency_ms')}`\n")
            f.write(f"- answer: `{r.get('answer')}`\n")
            f.write(f"- gold_answer: `{r.get('gold_answer')}`\n")
            f.write(f"- answer_correct: `{r.get('answer_correct')}`\n")
            f.write(f"- error_type: `{r.get('error_type')}`\n")
            f.write(f"- notes: `{r.get('notes', '')[:500]}`\n\n")

def write_w3_failure_cases(raw_csv: Path, failure_cases_md: Path, max_cases: int = 200) -> None:
    rows = read_csv(raw_csv)
    bad = [r for r in rows if r.get("correct_under_deadline") != "true"]

    with failure_cases_md.open("w", encoding="utf-8") as f:
        f.write("# W3 failure cases\n\n")
        f.write(
            "A row is treated as a failure when `correct_under_deadline != true`. "
            "The primary taxonomy separates strict JSON parsing, function-call envelope, "
            "action selection, and argument errors. `action_valid` independently records "
            "whether the predicted call conforms to its declared action schema.\n\n"
        )
        if not bad:
            f.write("No failure cases.\n")
            return

        for i, r in enumerate(bad[:max_cases], start=1):
            f.write(f"## {i}. {r.get('run_id')}\n\n")
            f.write(f"- sample_id: `{r.get('sample_id')}`\n")
            f.write(f"- performance_mode: `{r.get('performance_mode')}`\n")
            f.write(f"- deadline_ms: `{r.get('deadline_ms')}`\n")
            f.write(f"- time_to_valid_action_ms: `{r.get('time_to_valid_action_ms')}`\n")
            f.write(f"- action_valid: `{r.get('action_valid')}`\n")
            f.write(f"- action_correct: `{r.get('action_correct')}`\n")
            f.write(f"- action_schema_error: `{r.get('action_schema_error')}`\n")
            f.write(f"- predicted action: `{r.get('action_name')}`\n")
            f.write(f"- predicted arguments: `{r.get('action_arguments')}`\n")
            f.write(f"- gold action: `{r.get('gold_action')}`\n")
            f.write(f"- gold arguments: `{r.get('gold_arguments')}`\n")
            f.write(f"- error_type: `{r.get('error_type')}`\n")
            f.write(f"- notes: `{r.get('notes', '')[:800]}`\n\n")
