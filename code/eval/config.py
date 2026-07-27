import json
from pathlib import Path
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ResolvedPaths:
    config_path: Path
    repo_root: Path
    handoff_root: Path
    out_dir: Path
    raw_log_dir: Path
    runner_output_dir: Path
    raw_log_csv: Path
    summary_csv: Path
    thermal_summary_csv: Path
    energy_batch_csv: Path
    run_commands_md: Path
    failure_cases_md: Path
    samples_jsonl: Path
    tokenizer_path: Path
    tokenizer_config_path: Path
    pre_gen_pte: Path

def _resolve(path_value: str | Path, base: Path) -> Path:
    p = Path(path_value).expanduser()
    return p if p.is_absolute() else (base / p).resolve()

def require(cfg: dict[str, Any], dotted_key: str) -> Any:
    cur: Any = cfg
    for part in dotted_key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            raise KeyError(f"Missing config key: {dotted_key}")
        cur = cur[part]
    return cur

def resolve_paths(cfg: dict[str, Any], config_path: str | Path) -> ResolvedPaths:
    cpath = Path(config_path).expanduser().resolve()

    repo_root = _resolve(require(cfg, "paths.repo_root"), cpath.parent)
    handoff_root = _resolve(require(cfg, "paths.handoff_root"), repo_root)

    assignee = require(cfg, "assignee")
    task_group = require(cfg, "task_group")
    out_dir = handoff_root / assignee / task_group

    return ResolvedPaths(
        config_path=cpath,
        repo_root=repo_root,
        handoff_root=handoff_root,
        out_dir=out_dir,
        raw_log_dir=out_dir / "raw_runner_logs",
        runner_output_dir=out_dir / "runner_outputs",
        raw_log_csv=out_dir / "raw_logs.csv",
        summary_csv=out_dir / "summary_metrics.csv",
        thermal_summary_csv=out_dir / "thermal_summary_metrics.csv",
        energy_batch_csv=out_dir / "energy_batches.csv",
        run_commands_md=out_dir / "run_commands.md",
        failure_cases_md=out_dir / "failure_cases.md",
        samples_jsonl=_resolve(require(cfg, "paths.samples_jsonl"), repo_root),
        tokenizer_path=_resolve(require(cfg, "paths.tokenizer_path"), repo_root),
        tokenizer_config_path=_resolve(require(cfg, "paths.tokenizer_config_path"), repo_root),
        pre_gen_pte=_resolve(require(cfg, "paths.pre_gen_pte"), repo_root),
    )

def load_json_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path).expanduser().resolve()
    with path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    if not isinstance(cfg, dict):
        raise ValueError(f"Config must be a JSON object: {path}")
    return cfg

def ensure_output_dirs(paths: ResolvedPaths) -> None:
    paths.out_dir.mkdir(parents=True, exist_ok=True)
    paths.raw_log_dir.mkdir(parents=True, exist_ok=True)
    paths.runner_output_dir.mkdir(parents=True, exist_ok=True)
