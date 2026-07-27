import json
from pathlib import Path
from typing import Any


def read_streaming_samples(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Streaming samples file not found: {path}")

    samples: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            for key in ["sample_id", "prompt"]:
                if key not in row:
                    raise ValueError(f"Missing '{key}' in {path}:{line_no}")
            row.setdefault("dataset", "w1_manual_prompts")
            row.setdefault("difficulty", "unknown")
            samples.append(row)
    return samples


def build_streaming_prompt(sample: dict[str, Any], prompt_template: str) -> str:
    return prompt_template.format(**sample)
