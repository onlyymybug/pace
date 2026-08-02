#!/usr/bin/env python3
"""Run PACE W2 reasoning prompts with the deployed BitNet Hybrid-1024 stack."""

from __future__ import annotations

import argparse
import csv
import json
import shlex
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from tokenizers import Tokenizer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_w1 import (
    adb,
    adb_base,
    formatted_prompt_for_counting,
    parse_observer,
    required_env,
    sha256,
    shell_quote,
    stream_process,
)


PROMPT_TEMPLATE = (
    "Solve the math problem. Show your reasoning briefly. End with exactly: "
    "The answer is <scalar>. In that final sentence, <scalar> must be a plain "
    "integer, decimal, or a/b fraction. Do not use LaTeX, units, currency "
    "symbols, commas, or percent signs in the final answer.\n\n"
    "Problem: {question}"
)


def load_samples(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            missing = [
                key for key in ("sample_id", "question", "gold_answer") if key not in row
            ]
            if missing:
                raise ValueError(f"Missing {missing} at {path}:{line_number}")
            rows.append(row)
    return rows


def assistant_text(full_output: str) -> str:
    marker = "<|start_header_id|>assistant<|end_header_id|>"
    text = full_output.rsplit(marker, 1)[-1]
    for token in ("<|eot_id|>", "<|endoftext|>", "<|im_end|>"):
        text = text.replace(token, "")
    return text.strip()


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "sample_id",
        "dataset",
        "difficulty",
        "question",
        "gold_answer",
        "predicted_answer",
        "answer_parse_method",
        "answer_correct",
        "estimated_prompt_tokens",
        "runner_prompt_tokens",
        "seq_len_prompt_tokens",
        "prompt_token_source",
        "target_output_tokens",
        "seq_len",
        "generated_tokens",
        "decode_tokens_per_second",
        "ttft_ms",
        "inference_ms",
        "model_load_ms",
        "returncode",
        "output_path",
        "log_path",
        "error",
    ]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, help="run only the first N samples")
    parser.add_argument("--run-id", help="result directory name")
    parser.add_argument(
        "--model-max-seq-len",
        action="store_true",
        help="use the PTE maximum total sequence length instead of an output budget",
    )
    parser.add_argument(
        "--prompt-token-calibration-csv",
        type=Path,
        help="reuse runner_prompt_tokens from a previous run for exact output budgets",
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="continue after a failed sample",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")

    root = Path(required_env("BUNDLE_ROOT")).resolve()
    dataset_path = Path(required_env("W2_DATASET_PATH")).resolve()
    tokenizer_path = Path(required_env("TOKENIZER_PATH")).resolve()
    device_dir = required_env("DEVICE_DIR").rstrip("/")
    max_seq_len = int(required_env("MAX_SEQ_LEN"))
    target_output_tokens = int(required_env("W2_TARGET_OUTPUT_TOKENS"))
    seq_len_compensation = int(required_env("W2_SEQ_LEN_COMPENSATION"))
    run_id = args.run_id or f"w2_{datetime.now():%Y%m%d_%H%M%S}"
    result_dir = root / "results" / run_id
    result_dir.mkdir(parents=True, exist_ok=False)

    code_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(code_root))
    from support.w2_answer_parser import (  # pylint: disable=import-outside-toplevel
        answers_equal,
        parse_final_answer,
        parse_gold_answer,
    )

    samples = load_samples(dataset_path)
    if args.limit is not None:
        samples = samples[: args.limit]

    calibrated_prompt_tokens: dict[str, int] = {}
    calibration_path: Path | None = None
    if args.prompt_token_calibration_csv is not None:
        calibration_path = args.prompt_token_calibration_csv.resolve()
        with calibration_path.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                sample_id = row.get("sample_id", "")
                runner_count = row.get("runner_prompt_tokens", "")
                if sample_id and runner_count:
                    calibrated_prompt_tokens[sample_id] = int(runner_count)

    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    device_output_dir = f"{device_dir}/outputs/w2_hybrid_1024/{run_id}"
    adb("shell", f"mkdir -p {shell_quote(device_output_dir)}")

    manifest = {
        "run_id": run_id,
        "timestamp": datetime.now().astimezone().isoformat(),
        "task": "W2_reasoning",
        "device_serial": required_env("ANDROID_SERIAL"),
        "remote_model": f"{device_dir}/{required_env('REMOTE_MODEL_NAME')}",
        "local_model_sha256": sha256(root / "hybrid_llama_qnn.pte"),
        "dataset": str(dataset_path),
        "dataset_sha256": sha256(dataset_path),
        "qnn_version": "2.28.0.241029232508_102474",
        "model_mode": "hybrid",
        "max_seq_len": max_seq_len,
        "reasoning_budget_tokens": (
            "none" if args.model_max_seq_len else target_output_tokens
        ),
        "sequence_length_policy": (
            "model_max" if args.model_max_seq_len else "prompt_plus_output_budget"
        ),
        "seq_len_compensation": seq_len_compensation,
        "prompt_token_calibration_csv": (
            str(calibration_path) if calibration_path is not None else None
        ),
        "prompt_token_calibration_sha256": (
            sha256(calibration_path) if calibration_path is not None else None
        ),
        "budget_execution_mode": "physical",
        "htp_performance_mode": "runner_default_not_controllable",
        "token_timestamps": "unsupported_by_runner",
        "prompt_template": PROMPT_TEMPLATE,
    }
    (result_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    rows: list[dict[str, Any]] = []
    any_failure = False
    for index, sample in enumerate(samples, start=1):
        sample_id = str(sample["sample_id"])
        prompt = PROMPT_TEMPLATE.format(**sample)
        estimated_prompt_tokens = len(
            tokenizer.encode(formatted_prompt_for_counting(prompt)).ids
        )
        seq_len_prompt_tokens = estimated_prompt_tokens
        prompt_token_source = "host_tokenizer_estimate"
        if calibration_path is not None:
            if sample_id not in calibrated_prompt_tokens:
                raise RuntimeError(
                    f"{sample_id}: no runner_prompt_tokens in {calibration_path}"
                )
            seq_len_prompt_tokens = calibrated_prompt_tokens[sample_id]
            prompt_token_source = "previous_runner_observation"

        sample_output_capacity = target_output_tokens
        if args.model_max_seq_len:
            seq_len = max_seq_len
            sample_output_capacity = (
                max_seq_len - estimated_prompt_tokens - seq_len_compensation
            )
        elif calibration_path is not None:
            seq_len = seq_len_prompt_tokens + target_output_tokens + 1
        else:
            seq_len = (
                estimated_prompt_tokens
                + target_output_tokens
                + seq_len_compensation
            )
        if seq_len > max_seq_len:
            raise RuntimeError(
                f"{sample_id}: prompt({estimated_prompt_tokens}) + "
                f"budget({target_output_tokens}) exceeds {max_seq_len}"
            )

        sample_dir = result_dir / sample_id
        sample_dir.mkdir()
        remote_output = f"{device_output_dir}/{sample_id}_output.txt"
        remote_speed = f"{device_output_dir}/{sample_id}_inference_speed.txt"
        runner_args = [
            "./qnn_llama_runner",
            "--model_path",
            required_env("REMOTE_MODEL_NAME"),
            "--tokenizer_path",
            "tokenizer.json",
            "--prompt",
            prompt,
            "--system_prompt",
            "",
            "--seq_len",
            str(seq_len),
            "--eval_mode",
            required_env("EVAL_MODE"),
            "--kv_updater",
            required_env("KV_UPDATER"),
            "--temperature",
            required_env("TEMPERATURE"),
            "--logits_scale",
            required_env("LOGITS_SCALE"),
            "--logits_offset",
            required_env("LOGITS_OFFSET"),
            "--num_iters",
            "1",
            "--output_path",
            remote_output,
            "--performance_output_path",
            remote_speed,
        ]
        remote_command = "\n".join(
            [
                f"cd {shell_quote(device_dir)} || exit 1",
                'export LD_LIBRARY_PATH="$PWD"',
                'export LD_PRELOAD="$PWD/libc++_shared.so"',
                'export ADSP_LIBRARY_PATH="$PWD${ADSP_LIBRARY_PATH:+;$ADSP_LIBRARY_PATH}"',
                "unset QNN_OP_PACKAGE_PATHS",
                shlex.join(runner_args),
            ]
        )
        command = [*adb_base(), "shell", remote_command]
        (sample_dir / "command.txt").write_text(
            shlex.join(command) + "\n", encoding="utf-8"
        )

        print(
            f"\n[{index}/{len(samples)}] {sample_id}: "
            f"prompt_tokens={estimated_prompt_tokens} seq_len={seq_len}",
            flush=True,
        )
        log_path = sample_dir / "run.log"
        returncode = stream_process(command, log_path)
        error = ""
        output_path = sample_dir / "output.txt"
        speed_path = sample_dir / "inference_speed.txt"
        if returncode == 0:
            for remote_path, local_path in (
                (remote_output, output_path),
                (remote_speed, speed_path),
            ):
                pulled = adb(
                    "pull",
                    "-a",
                    remote_path,
                    str(local_path),
                    check=False,
                    capture_output=True,
                )
                if pulled.returncode != 0:
                    returncode = pulled.returncode
                    error = pulled.stderr.strip() or pulled.stdout.strip()
                    break

        log_text = log_path.read_text(encoding="utf-8", errors="replace")
        observer = parse_observer(log_text)
        predicted_answer = "NA"
        parse_method = "no_output"
        answer_correct = False
        if output_path.exists():
            generated = assistant_text(
                output_path.read_text(encoding="utf-8", errors="replace")
            )
            parsed = parse_final_answer(generated)
            gold = parse_gold_answer(sample["gold_answer"])
            predicted_answer = parsed.answer
            parse_method = parsed.method
            answer_correct = answers_equal(parsed.answer, gold.answer)
            (sample_dir / "assistant.txt").write_text(
                generated + "\n", encoding="utf-8"
            )

        def elapsed(start_key: str, end_key: str) -> int | str:
            if start_key not in observer or end_key not in observer:
                return ""
            return int(observer[end_key]) - int(observer[start_key])

        rows.append(
            {
                "sample_id": sample_id,
                "dataset": sample.get("dataset", ""),
                "difficulty": sample.get("difficulty", ""),
                "question": sample["question"],
                "gold_answer": sample["gold_answer"],
                "predicted_answer": predicted_answer,
                "answer_parse_method": parse_method,
                "answer_correct": answer_correct,
                "estimated_prompt_tokens": estimated_prompt_tokens,
                "runner_prompt_tokens": observer.get("prompt_tokens", ""),
                "seq_len_prompt_tokens": seq_len_prompt_tokens,
                "prompt_token_source": prompt_token_source,
                "target_output_tokens": sample_output_capacity,
                "seq_len": seq_len,
                "generated_tokens": observer.get("generated_tokens", ""),
                "decode_tokens_per_second": observer.get(
                    "decode_token_per_sec", observer.get("tokens_per_second", "")
                ),
                "ttft_ms": elapsed("inference_start_ms", "first_token_ms"),
                "inference_ms": elapsed("inference_start_ms", "inference_end_ms"),
                "model_load_ms": elapsed("model_load_start_ms", "model_load_end_ms"),
                "returncode": returncode,
                "output_path": str(output_path),
                "log_path": str(log_path),
                "error": error or ("" if returncode == 0 else "runner_failed"),
            }
        )
        write_summary(result_dir / "summary.csv", rows)
        if returncode != 0:
            any_failure = True
            if not args.continue_on_error:
                break

    print(f"\nResults: {result_dir}")
    print(f"Summary: {result_dir / 'summary.csv'}")
    return 1 if any_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
