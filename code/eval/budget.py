from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .metrics import to_float_or_none


PHYSICAL_BUDGET_MODE = "physical"
SIMULATED_TRUNCATION_BUDGET_MODE = "simulated_truncation"
_BUDGET_MODES = {
    PHYSICAL_BUDGET_MODE,
    SIMULATED_TRUNCATION_BUDGET_MODE,
}


@dataclass(frozen=True)
class BudgetView:
    text: str
    output_timestamp_count: int
    completion_latency_ms: Any
    truncated: bool


def resolve_budget_execution_mode(experiment: dict[str, Any]) -> str:
    mode = str(experiment.get("budget_execution_mode", PHYSICAL_BUDGET_MODE))
    if mode not in _BUDGET_MODES:
        choices = ", ".join(sorted(_BUDGET_MODES))
        raise ValueError(
            f"Unsupported experiment.budget_execution_mode={mode!r}; expected one of: {choices}"
        )
    return mode


def physical_budgets(budgets: list[int], mode: str) -> list[int]:
    if not budgets:
        raise ValueError("At least one budget is required")
    if any(budget <= 0 for budget in budgets):
        raise ValueError(f"Budgets must be positive: {budgets}")
    if len(set(budgets)) != len(budgets):
        raise ValueError(f"Budgets must be unique: {budgets}")
    if mode == SIMULATED_TRUNCATION_BUDGET_MODE:
        return [max(budgets)]
    if mode == PHYSICAL_BUDGET_MODE:
        return budgets
    raise ValueError(f"Unsupported budget execution mode: {mode!r}")


def build_budget_view(token_timestamps_path: Path, budget: int) -> BudgetView:
    if budget <= 0:
        raise ValueError(f"Budget must be positive: {budget}")
    if not token_timestamps_path.exists():
        raise RuntimeError(
            "Simulated budget truncation requires token timestamps, but the file is missing: "
            f"{token_timestamps_path}"
        )

    rows: list[dict[str, Any]] = []
    with token_timestamps_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                rows.append(row)

    output_rows = [row for row in rows if not bool(row.get("prompt_echo", False))]
    if not output_rows:
        raise RuntimeError(
            "Simulated budget truncation requires output token timestamps, but none were found: "
            f"{token_timestamps_path}"
        )

    selected_rows = output_rows[:budget]
    last_row = selected_rows[-1]
    completion_latency_ms = to_float_or_none(last_row.get("delta_ms"))
    if completion_latency_ms is None:
        first_timestamp_ms = next(
            (
                value
                for row in rows
                if (value := to_float_or_none(row.get("timestamp_ms"))) is not None
            ),
            None,
        )
        last_timestamp_ms = to_float_or_none(last_row.get("timestamp_ms"))
        if first_timestamp_ms is not None and last_timestamp_ms is not None:
            completion_latency_ms = last_timestamp_ms - first_timestamp_ms

    if completion_latency_ms is None:
        raise RuntimeError(
            "Simulated budget truncation requires delta_ms or timestamp_ms values: "
            f"{token_timestamps_path}"
        )

    return BudgetView(
        text="".join(str(row.get("piece", "")) for row in selected_rows),
        output_timestamp_count=len(selected_rows),
        completion_latency_ms=completion_latency_ms,
        truncated=len(output_rows) > budget,
    )
