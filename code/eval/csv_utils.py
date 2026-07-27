import csv
from pathlib import Path
from typing import Any

from .constants import NA


def append_csv(path: Path, row: dict[str, Any], columns: list[str]) -> None:
    write_header = not path.exists()
    if not write_header:
        with path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_columns = reader.fieldnames or []
            existing_rows = list(reader)
        if existing_columns != columns:
            if any(column not in columns for column in existing_columns):
                raise ValueError(f"Existing CSV has incompatible columns: {path}")
            write_csv(path, existing_rows, columns)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        if write_header:
            writer.writeheader()
        writer.writerow({k: row.get(k, NA) for k in columns})


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, NA) for k in columns})
