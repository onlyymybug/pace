#!/usr/bin/env python3
"""Run one complete W1/W2/W3 pass with the deployed QNN 2.37 Qwen bundle."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

from tokenizers import Tokenizer


SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLE = Path(
    os.environ.get("QWEN_BUNDLE_ROOT", "/home/lyyyy/qwen25_3b_phone_bundle")
).resolve()
PACE_CODE = Path(
    os.environ.get("PACE_CODE_ROOT", str(SCRIPT_DIR.parent))
).resolve()

from support.w2_answer_parser import answers_equal, parse_final_answer, parse_gold_answer
from support.w3_action_data import build_action_prompt
from support.w3_action_validator import classify_action, parse_action_text, validate_action_schema


ADB = Path(
    os.environ.get(
        "ADB_BIN",
        "/mnt/c/Users/lyyyy/AppData/Local/Microsoft/WinGet/Packages/"
        "Google.PlatformTools_Microsoft.Winget.Source_8wekyb3d8bbwe/platform-tools/adb.exe",
    )
)
ADB_SERVER_PORT = os.environ.get("ADB_SERVER_PORT", "5037")
SERIAL = os.environ.get("ANDROID_SERIAL", "3B15B800A0R00000")
PHONE_DIR = os.environ.get(
    "PHONE_DIR", "/data/local/tmp/lyy/executorch/qwen25_3b_qnn237_block16"
)
OBSERVER_RE = re.compile(r"PyTorchObserver\s+(\{.*?\})")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def windows_path(path: Path) -> str:
    return subprocess.check_output(
        ["wslpath", "-w", str(path.resolve())], text=True
    ).strip()


def adb(*args: str, timeout: int = 240) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ADB), "-P", ADB_SERVER_PORT, "-s", SERIAL, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def observer_metrics(log_text: str) -> dict[str, Any]:
    match = OBSERVER_RE.search(log_text)
    if not match:
        return {}
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}
    start = data.get("inference_start_ms")
    end = data.get("inference_end_ms")
    first = data.get("first_token_ms")
    load_start = data.get("model_load_start_ms")
    load_end = data.get("model_load_end_ms")
    data["model_load_ms"] = (
        load_end - load_start if load_start is not None and load_end is not None else None
    )
    data["ttft_ms"] = first - start if first is not None and start is not None else None
    data["e2e_latency_ms"] = end - start if end is not None and start is not None else None
    return data


def completion_from_output(raw: str, prompt: str) -> str:
    if raw.startswith(prompt):
        return raw[len(prompt) :].lstrip()
    return raw


def prompt_for(task: str, sample: dict[str, Any], cfg: dict[str, Any]) -> str:
    template = cfg["experiment"]["prompt_template"]
    if task == "W1":
        return template.format(prompt=sample["prompt"])
    if task == "W2":
        return template.format(question=sample["question"])
    return build_action_prompt(sample, template, cfg["experiment"]["action_schema"])


def score(task: str, sample: dict[str, Any], completion: str, cfg: dict[str, Any]) -> dict[str, Any]:
    if task == "W1":
        nonempty = bool(completion.strip())
        return {"output_nonempty": nonempty, "score_correct": ""}
    if task == "W2":
        parsed = parse_final_answer(completion)
        gold = parse_gold_answer(sample["gold_answer"])
        correct = answers_equal(parsed.answer, gold.answer)
        return {
            "predicted_answer": parsed.answer,
            "gold_answer": gold.answer,
            "answer_parse_method": parsed.method,
            "score_correct": correct,
        }
    schema = cfg["experiment"]["action_schema"]
    parsed = parse_action_text(completion)
    validation = validate_action_schema(parsed, schema)
    valid, correct, error_type, message = classify_action(
        parsed, validation, sample["gold_action"], sample["gold_arguments"]
    )
    return {
        "predicted_action": parsed.action,
        "gold_action": sample["gold_action"],
        "action_valid": valid,
        "action_error_type": error_type,
        "action_error_message": message,
        "score_correct": correct,
    }


def run_sample(
    *,
    task: str,
    sample: dict[str, Any],
    cfg: dict[str, Any],
    budget: int,
    tokenizer: Tokenizer,
    remote_root: str,
    local_root: Path,
) -> dict[str, Any]:
    sample_id = sample["sample_id"]
    prompt = prompt_for(task, sample, cfg)
    estimated_prompt_tokens = len(tokenizer.encode(prompt).ids)
    seq_len = estimated_prompt_tokens + budget
    if seq_len > 1024:
        raise ValueError(f"{sample_id}: seq_len={seq_len} exceeds 1024")

    remote_dir = f"{remote_root}/{task.lower()}/{sample_id}"
    local_dir = local_root / task.lower() / sample_id
    local_dir.mkdir(parents=True, exist_ok=True)
    (local_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    runner_args = [
        "./qnn_llama_runner",
        "--decoder_model_version", "qwen2_5",
        "--model_path", "hybrid_llama_qnn.pte",
        "--tokenizer_path", "tokenizer.json",
        "--prompt", prompt,
        "--system_prompt", "",
        "--seq_len", str(seq_len),
        "--eval_mode", "1",
        "--temperature", "0",
        "--num_iters", "1",
        "--shared_buffer",
        "--output_path", f"{remote_dir}/generated_text.txt",
        "--performance_output_path", f"{remote_dir}/speed.txt",
    ]
    command = " ".join(
        [
            f"cd {shlex.quote(PHONE_DIR)} || exit 1;",
            f"mkdir -p {shlex.quote(remote_dir)};",
            f"rm -f {shlex.quote(remote_dir + '/generated_text.txt')} "
            f"{shlex.quote(remote_dir + '/speed.txt')} {shlex.quote(remote_dir + '/runner.log')};",
            "export LD_LIBRARY_PATH=$PWD;",
            "export ADSP_LIBRARY_PATH=$PWD;",
            "export QNN_OP_PACKAGE_PATHS='';",
            "{",
            shlex.join(runner_args) + ";",
            "runner_rc=$?;",
            'printf "\\nrunner_returncode=%s\\n" "$runner_rc";',
            'exit "$runner_rc";',
            f"}} > {shlex.quote(remote_dir + '/runner.log')} 2>&1",
        ]
    )
    shell_result = adb("shell", command)
    pull_result = adb("pull", "-a", remote_dir + "/.", windows_path(local_dir))

    log_path = local_dir / "runner.log"
    output_path = local_dir / "generated_text.txt"
    log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    raw_output = output_path.read_text(encoding="utf-8", errors="replace") if output_path.exists() else ""
    completion = completion_from_output(raw_output, prompt)
    (local_dir / "completion.txt").write_text(completion, encoding="utf-8")

    metrics = observer_metrics(log_text)
    rc_match = re.search(r"runner_returncode=(\d+)", log_text)
    runner_rc = int(rc_match.group(1)) if rc_match else shell_result.returncode
    row: dict[str, Any] = {
        "task": task,
        "sample_id": sample_id,
        "budget_tokens": budget,
        "estimated_prompt_tokens": estimated_prompt_tokens,
        "seq_len": seq_len,
        "runner_returncode": runner_rc,
        "adb_pull_returncode": pull_result.returncode,
        "prompt_tokens": metrics.get("prompt_tokens"),
        "generated_tokens": metrics.get("generated_tokens"),
        "model_load_ms": metrics.get("model_load_ms"),
        "ttft_ms": metrics.get("ttft_ms"),
        "e2e_latency_ms": metrics.get("e2e_latency_ms"),
        "prefill_token_per_sec": metrics.get("prefill_token_per_sec"),
        "decode_token_per_sec": metrics.get("decode_token_per_sec"),
        "seq_len_stop": "Generation stopped at seq_len limit" in log_text,
        "qnn_shards_restored": log_text.count(
            "Use cached delegate handle for current method: kv_forward"
        ),
        "output_chars": len(completion),
        "replacement_chars": completion.count("\ufffd"),
    }
    row.update(score(task, sample, completion, cfg))
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for task in ("W1", "W2", "W3"):
        selected = [row for row in rows if row["task"] == task]
        correct_values = [row.get("score_correct") for row in selected]
        scored = [value for value in correct_values if isinstance(value, bool)]
        numeric = lambda key: [float(row[key]) for row in selected if row.get(key) is not None]
        summary[task] = {
            "samples": len(selected),
            "runtime_successes": sum(row["runner_returncode"] == 0 for row in selected),
            "scored_samples": len(scored),
            "correct": sum(scored),
            "accuracy": sum(scored) / len(scored) if scored else None,
            "mean_ttft_ms": mean(numeric("ttft_ms")) if numeric("ttft_ms") else None,
            "mean_e2e_latency_ms": mean(numeric("e2e_latency_ms")) if numeric("e2e_latency_ms") else None,
            "mean_decode_token_per_sec": (
                mean(numeric("decode_token_per_sec")) if numeric("decode_token_per_sec") else None
            ),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default=datetime.now().strftime("%Y%m%d_%H%M%S"))
    args = parser.parse_args()

    device = adb("devices", "-l", timeout=15)
    if SERIAL not in device.stdout or "device" not in device.stdout:
        print(device.stdout, end="")
        raise RuntimeError("phone is not connected through Windows adb")

    tokenizer = Tokenizer.from_file(str(BUNDLE / "model/tokenizer.json"))
    definitions = [
        ("W1", "w1_streaming_samples.jsonl", "run_w1_streaming_config.json", 512),
        ("W2", "w2_reasoning_samples.jsonl", "run_w2_reasoning_config.json", 128),
        ("W3", "w3_action_samples.jsonl", "run_w3_action_config.json", 96),
    ]
    local_root = BUNDLE / "results" / f"pace_w1_w2_w3_{args.tag}"
    local_root.mkdir(parents=True, exist_ok=True)
    remote_root = f"{PHONE_DIR}/outputs/pace_w1_w2_w3_{args.tag}"
    rows: list[dict[str, Any]] = []

    manifest = {
        "tag": args.tag,
        "serial": SERIAL,
        "phone_dir": PHONE_DIR,
        "decoder_model_version": "qwen2_5",
        "eval_mode": 1,
        "temperature": 0,
        "shared_buffer": True,
        "qnn_op_package_paths": "",
        "runs": {task: {"budget": budget} for task, _, _, budget in definitions},
    }
    (local_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    total = sum(len(load_jsonl(PACE_CODE / "data" / data)) for _, data, _, _ in definitions)
    completed = 0
    for task, data_name, cfg_name, budget in definitions:
        samples = load_jsonl(PACE_CODE / "data" / data_name)
        cfg = load_json(SCRIPT_DIR / cfg_name)
        for sample in samples:
            completed += 1
            row = run_sample(
                task=task,
                sample=sample,
                cfg=cfg,
                budget=budget,
                tokenizer=tokenizer,
                remote_root=remote_root,
                local_root=local_root,
            )
            rows.append(row)
            write_csv(local_root / "summary.csv", rows)
            correctness = row.get("score_correct", "unscored")
            print(
                f"[{completed}/{total}] {task} {row['sample_id']} rc={row['runner_returncode']} "
                f"prompt={row.get('prompt_tokens')} gen={row.get('generated_tokens')} "
                f"ttft={row.get('ttft_ms')}ms decode={row.get('decode_token_per_sec')} "
                f"correct={correctness}",
                flush=True,
            )

    summary = summarize(rows)
    (local_root / "aggregate.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"results={local_root}")
    return 0 if all(row["runner_returncode"] == 0 for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
