from typing import Any
from pathlib import Path
import json

def read_reasoning_samples(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Reasoning samples file not found: {path}")

    samples: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            for key in ["sample_id", "question", "gold_answer"]:
                if key not in row:
                    raise ValueError(f"Missing '{key}' in {path}:{line_no}")
            if "dataset" not in row:
                row["dataset"] = "unknown"
            if "difficulty" not in row:
                row["difficulty"] = "unknown"
            samples.append(row)
    return samples

def build_reasoning_prompt(sample: dict[str, Any], prompt_template: str) -> str:
    return prompt_template.format(**sample)