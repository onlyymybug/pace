"""Dataset adapters and conservative scoring for GSM8K and MATH-500."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


GSM8K_PROMPT_TEMPLATE = (
    "Solve the grade-school math problem. Show your reasoning briefly. End with "
    "exactly: The answer is <scalar>. In that final sentence, <scalar> must be "
    "a plain integer, decimal, or a/b fraction. Do not use LaTeX, units, currency "
    "symbols, commas, or percent signs in the final answer.\n\nProblem: {question}"
)

MATH500_PROMPT_TEMPLATE = (
    "Solve the competition mathematics problem. Show your reasoning briefly. "
    "End with exactly: Final answer: \\boxed{{<answer>}}. Put only the final "
    "mathematical expression inside \\boxed{{}}.\n\nProblem: {question}"
)

_INTEGER = r"(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)"
_NUMBER = (
    rf"[-+]?(?:{_INTEGER}\s*/\s*[-+]?{_INTEGER}|"
    rf"{_INTEGER}(?:\.[0-9]+)?|\.[0-9]+)"
)
_FINAL_NUMERIC_RE = re.compile(
    rf"The\s+answer\s+is\s+({_NUMBER})\s*\.?\s*(?:<\|[^>]+\|>)?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_GSM8K_GOLD_RE = re.compile(rf"####\s*({_NUMBER})\s*$", re.MULTILINE)


@dataclass(frozen=True)
class BenchmarkSpec:
    name: str
    default_budget: int
    prompt_template: str


BENCHMARKS = {
    "GSM8K": BenchmarkSpec("GSM8K", 128, GSM8K_PROMPT_TEMPLATE),
    "MATH500": BenchmarkSpec("MATH500", 256, MATH500_PROMPT_TEMPLATE),
}


def canonical_benchmark_name(value: str) -> str:
    name = value.upper().replace("-", "")
    if name == "MATH500":
        return "MATH500"
    if name == "GSM8K":
        return "GSM8K"
    raise ValueError(f"Unsupported benchmark: {value}")


def load_benchmark_samples(path: Path, benchmark: str) -> list[dict[str, Any]]:
    """Load a source JSONL file into the common runner sample schema."""
    benchmark = canonical_benchmark_name(benchmark)
    samples: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for index, line in enumerate(stream, 1):
            if not line.strip():
                continue
            source = json.loads(line)
            if benchmark == "GSM8K":
                required = ("question", "answer")
                question = source.get("question")
                gold_solution = source.get("answer")
                gold_answer = _last_gsm8k_gold(str(gold_solution or ""))
                subject = "Grade School Math"
                difficulty: Any = ""
                source_id = str(index)
            else:
                required = ("problem", "answer", "unique_id")
                question = source.get("problem")
                gold_solution = source.get("solution", "")
                gold_answer = source.get("answer")
                subject = source.get("subject", "")
                difficulty = source.get("level", "")
                source_id = str(source.get("unique_id", index))

            missing = [key for key in required if key not in source]
            if missing:
                raise ValueError(f"Missing {missing} at {path}:{index}")
            if not question or gold_answer in (None, ""):
                raise ValueError(f"Empty question/answer at {path}:{index}")

            samples.append(
                {
                    "sample_id": f"{benchmark.lower()}_{index:04d}",
                    "dataset": benchmark,
                    "source_id": source_id,
                    "subject": subject,
                    "difficulty": difficulty,
                    "question": str(question),
                    "gold_answer": str(gold_answer),
                    "gold_solution": str(gold_solution or ""),
                }
            )
    return samples


def build_benchmark_prompt(benchmark: str, question: str) -> str:
    spec = BENCHMARKS[canonical_benchmark_name(benchmark)]
    return spec.prompt_template.format(question=question)


def score_benchmark_answer(
    benchmark: str, completion: str, gold_answer: str
) -> dict[str, Any]:
    """Score GSM8K numerically and MATH-500 by normalized exact match.

    MATH-500 symbolic equivalence requires a dedicated verifier. The conservative
    normalized exact result is deliberately labelled so it is not confused with
    the official benchmark metric.
    """
    benchmark = canonical_benchmark_name(benchmark)
    if benchmark == "GSM8K":
        matches = _FINAL_NUMERIC_RE.findall(completion or "")
        predicted = _normalize_number(matches[-1]) if matches else "NA"
        gold = _normalize_number(gold_answer)
        return {
            "predicted_answer": predicted,
            "gold_answer": gold,
            "normalized_predicted_answer": predicted,
            "normalized_gold_answer": gold,
            "answer_parse_method": (
                "exact_answer_phrase" if matches else "missing_answer_marker"
            ),
            "score_method": "gsm8k_numeric_exact",
            "score_correct": predicted != "NA" and predicted == gold,
        }

    predicted, parse_method = _extract_math500_answer(completion or "")
    normalized_predicted = _normalize_math_expression(predicted)
    normalized_gold = _normalize_math_expression(gold_answer)
    return {
        "predicted_answer": predicted or "NA",
        "gold_answer": gold_answer,
        "normalized_predicted_answer": normalized_predicted or "NA",
        "normalized_gold_answer": normalized_gold or "NA",
        "answer_parse_method": parse_method,
        "score_method": "math500_normalized_exact_not_symbolic_equivalence",
        "score_correct": bool(normalized_predicted)
        and normalized_predicted == normalized_gold,
    }


def _last_gsm8k_gold(text: str) -> str:
    matches = _GSM8K_GOLD_RE.findall(text)
    if not matches:
        raise ValueError("GSM8K answer does not contain a trailing #### value")
    return matches[-1]


def _normalize_number(value: Any) -> str:
    text = str(value).strip().replace(",", "").replace("$", "")
    text = re.sub(r"\s+", "", text)
    try:
        if "/" in text:
            numerator, denominator = text.split("/", 1)
            number = Decimal(numerator) / Decimal(denominator)
        else:
            number = Decimal(text)
    except (InvalidOperation, ValueError, ZeroDivisionError):
        return "NA"
    if number == number.to_integral_value():
        return str(number.quantize(Decimal(1)))
    return format(number.normalize(), "f").rstrip("0").rstrip(".")


def _extract_math500_answer(text: str) -> tuple[str, str]:
    boxed_answers: list[str] = []
    marker = r"\boxed{"
    start = 0
    while True:
        marker_index = text.find(marker, start)
        if marker_index < 0:
            break
        content_start = marker_index + len(marker)
        depth = 1
        index = content_start
        while index < len(text) and depth:
            if text[index] == "{" and (index == 0 or text[index - 1] != "\\"):
                depth += 1
            elif text[index] == "}" and (index == 0 or text[index - 1] != "\\"):
                depth -= 1
            index += 1
        if depth == 0:
            boxed_answers.append(text[content_start : index - 1])
            start = index
        else:
            break
    if boxed_answers:
        return boxed_answers[-1].strip(), "last_boxed_answer"

    matches = re.findall(
        r"Final\s+answer\s*:\s*(.+?)\s*(?:<\|[^>]+\|>|$)",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if matches:
        return matches[-1].strip().rstrip("."), "final_answer_fallback"
    return "", "missing_boxed_answer"


def _normalize_math_expression(value: Any) -> str:
    text = str(value).strip()
    text = text.replace("$", "")
    text = text.replace(r"\left", "").replace(r"\right", "")
    text = text.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    text = text.replace(r"\,", "").replace(r"\!", "")
    text = text.replace("−", "-").replace("–", "-")
    text = re.sub(r"\s+", "", text)
    while len(text) >= 2 and (
        (text[0], text[-1]) in (("$", "$"), ("{", "}"))
        and _outer_pair_wraps_entire_expression(text)
    ):
        text = text[1:-1]
    return text.rstrip(".").lower()


def _outer_pair_wraps_entire_expression(text: str) -> bool:
    if not text:
        return False
    opening, closing = text[0], text[-1]
    expected = {"{": "}", "$": "$"}.get(opening)
    if expected != closing:
        return False
    if opening == "$":
        return text.count("$") == 2
    depth = 0
    for index, char in enumerate(text):
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0 and index != len(text) - 1:
                return False
    return depth == 0
