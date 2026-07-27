import argparse
import getpass
import shlex
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, TextIO


MODE_CONFIG = {
    "kv": (0, "kv_llama_qnn.pte"),
    "hybrid": (1, "hybrid_llama_qnn.pte"),
}

DECODER_MODEL_VERSIONS = {
    "qwen2_5-3b_instruct": "qwen2_5_instruct",
}

OUTPUT_FILENAMES = (
    "outputs.txt",
    "inference_speed.txt",
    "token_timestamps.jsonl",
)


def default_device_workspace() -> str:
    return f"/data/local/tmp/{getpass.getuser()}/executorch/static_llm"


@dataclass(frozen=True)
class QnnPteRunSpec:
    device: str
    artifact: Path
    decoder_model: str
    model_mode: str
    prompt: str
    max_seq_len: int
    temperature: float = 0.0
    htp_performance_mode: int = 2
    system_prompt: str = ""
    adb: str = "adb"
    device_workspace: str = field(default_factory=default_device_workspace)


@dataclass(frozen=True)
class QnnPteRunResult:
    returncode: int
    output_dir: Path
    output_text_path: Path
    inference_speed_path: Path
    token_timestamps_path: Path


def build_runner_command(spec: QnnPteRunSpec) -> str:
    eval_mode, pte_filename = MODE_CONFIG[spec.model_mode]
    workspace = spec.device_workspace.rstrip("/")
    device_output_dir = f"{workspace}/outputs"

    runner_args = [
        "./qnn_llama_runner",
        "--decoder_model_version",
        DECODER_MODEL_VERSIONS[spec.decoder_model],
        "--tokenizer_path",
        workspace,
        "--model_path",
        f"{workspace}/{pte_filename}",
        "--output_path",
        f"{device_output_dir}/outputs.txt",
        "--performance_output_path",
        f"{device_output_dir}/inference_speed.txt",
        "--token_timestamps_output_path",
        f"{device_output_dir}/token_timestamps.jsonl",
        "--shared_buffer",
        "--htp_performance_mode",
        str(spec.htp_performance_mode),
        "--eval_mode",
        str(eval_mode),
        "--temperature",
        str(spec.temperature),
        "--seq_len",
        str(spec.max_seq_len),
        "--prompt",
        spec.prompt,
    ]
    if spec.system_prompt:
        runner_args.extend(["--system_prompt", spec.system_prompt])

    return " && ".join(
        [
            shlex.join(["mkdir", "-p", device_output_dir]),
            shlex.join(["cd", workspace]),
            shlex.join(runner_args),
        ]
    )


def _result(returncode: int, output_dir: Path) -> QnnPteRunResult:
    return QnnPteRunResult(
        returncode=returncode,
        output_dir=output_dir,
        output_text_path=output_dir / "outputs.txt",
        inference_speed_path=output_dir / "inference_speed.txt",
        token_timestamps_path=output_dir / "token_timestamps.jsonl",
    )


def _require_device_path(
    spec: QnnPteRunSpec, path: str, *, executable: bool = False
) -> None:
    test_flag = "-x" if executable else "-e"
    result = subprocess.run(
        [
            spec.adb,
            "-s",
            spec.device,
            "shell",
            f"test {test_flag} {shlex.quote(path)}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        raise FileNotFoundError(f"required device path is missing: {path}")


def _run_streamed(command: list[str], emit: Callable[[str], None]) -> int:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert process.stdout is not None
    for line in process.stdout:
        emit(line)
    process.wait()
    return int(process.returncode)


def _prepare_output_dir(output_dir: Path) -> Path:
    partial_dir = output_dir.with_name(f".{output_dir.name}.partial")
    for path in (partial_dir, output_dir):
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    partial_dir.mkdir(parents=True)
    return partial_dir


def _write_log_header(
    log_file: TextIO | None, spec: QnnPteRunSpec, output_dir: Path
) -> None:
    if log_file is None:
        return
    log_file.write(
        "$ run_qnn_pte "
        + shlex.join(
            [
                "--device",
                spec.device,
                "--model-mode",
                spec.model_mode,
                "--decoder-model",
                spec.decoder_model,
                "--max-seq-len",
                str(spec.max_seq_len),
                "--temperature",
                str(spec.temperature),
                "--htp-performance-mode",
                str(spec.htp_performance_mode),
                "--output-dir",
                str(output_dir),
                "--prompt",
                spec.prompt,
            ]
        )
        + "\n\n"
    )
    log_file.flush()


def run_qnn_pte(
    spec: QnnPteRunSpec,
    *,
    output_dir: Path,
    log_path: Path | None = None,
) -> QnnPteRunResult:
    output_dir = output_dir.resolve()
    log_file = None
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file = log_path.open("w", encoding="utf-8")

    returncode = 1
    partial_dir: Path | None = None

    def emit(text: str) -> None:
        print(text, end="", flush=True)
        if log_file is not None:
            log_file.write(text)
            log_file.flush()

    try:
        _write_log_header(log_file, spec, output_dir)
        partial_dir = _prepare_output_dir(output_dir)
        if spec.model_mode not in MODE_CONFIG:
            raise ValueError(f"unsupported model mode: {spec.model_mode}")
        if spec.decoder_model not in DECODER_MODEL_VERSIONS:
            raise ValueError(f"unsupported decoder model: {spec.decoder_model}")
        if not 0 <= spec.htp_performance_mode <= 8:
            raise ValueError("htp_performance_mode must be between 0 and 8")

        _, pte_filename = MODE_CONFIG[spec.model_mode]
        local_pte_path = spec.artifact / pte_filename
        if not local_pte_path.is_file():
            raise FileNotFoundError(f"pre-generated PTE not found: {local_pte_path}")

        workspace = spec.device_workspace.rstrip("/")
        device_runner = f"{workspace}/qnn_llama_runner"
        device_pte = f"{workspace}/{pte_filename}"
        _require_device_path(spec, device_runner, executable=True)
        _require_device_path(spec, device_pte)
        _require_device_path(spec, f"{workspace}/tokenizer.json")
        _require_device_path(spec, f"{workspace}/tokenizer_config.json")

        emit(
            f"[qnn_pte_runner] mode={spec.model_mode} device={spec.device} "
            f"pte={device_pte}\n"
        )

        returncode = _run_streamed(
            [spec.adb, "-s", spec.device, "shell", build_runner_command(spec)],
            emit,
        )
        if returncode != 0:
            raise subprocess.CalledProcessError(returncode, "adb shell")

        device_output_dir = f"{workspace}/outputs"
        for filename in OUTPUT_FILENAMES:
            returncode = _run_streamed(
                [
                    spec.adb,
                    "-s",
                    spec.device,
                    "pull",
                    "-a",
                    f"{device_output_dir}/{filename}",
                    str(partial_dir / filename),
                ],
                emit,
            )
            if returncode != 0:
                raise subprocess.CalledProcessError(returncode, f"adb pull {filename}")

        partial_dir.replace(output_dir)
        partial_dir = None
        output_text = (output_dir / "outputs.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        emit(f"Device Inference Results[0]:\n{output_text}\n")
        emit(f"[qnn_pte_runner] finished {spec.model_mode} inference\n")
        returncode = 0
    except (
        FileNotFoundError,
        OSError,
        ValueError,
        subprocess.CalledProcessError,
    ) as error:
        if returncode == 0:
            returncode = 1
        emit(f"[qnn_pte_runner] ERROR: {error}\n")
    finally:
        if partial_dir is not None and partial_dir.exists():
            shutil.rmtree(partial_dir)
        if log_file is not None:
            log_file.write(f"\n[qnn_pte_runner] returncode = {returncode}\n")
            log_file.close()

    return _result(returncode, output_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run an already-deployed QNN Llama PTE without pushing files."
    )
    parser.add_argument("--device", required=True)
    parser.add_argument("--artifact", required=True, type=Path)
    parser.add_argument("--output_dir", required=True, type=Path)
    parser.add_argument("--log_path", type=Path)
    parser.add_argument(
        "--decoder_model", choices=DECODER_MODEL_VERSIONS, required=True
    )
    parser.add_argument("--model_mode", choices=MODE_CONFIG, required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--max_seq_len", required=True, type=int)
    parser.add_argument("--temperature", default=0.0, type=float)
    parser.add_argument("--htp_performance_mode", default=2, type=int, choices=range(9))
    parser.add_argument("--system_prompt", default="")
    parser.add_argument("--adb", default="adb")
    parser.add_argument("--device_workspace", default=default_device_workspace())
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = run_qnn_pte(
        QnnPteRunSpec(
            device=args.device,
            artifact=args.artifact,
            decoder_model=args.decoder_model,
            model_mode=args.model_mode,
            prompt=args.prompt,
            max_seq_len=args.max_seq_len,
            temperature=args.temperature,
            htp_performance_mode=args.htp_performance_mode,
            system_prompt=args.system_prompt,
            adb=args.adb,
            device_workspace=args.device_workspace,
        ),
        output_dir=args.output_dir,
        log_path=args.log_path,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
