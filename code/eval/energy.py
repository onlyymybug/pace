from __future__ import annotations

import re
import subprocess
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .constants import NA
from .metrics import fmt


_INTEGER_LINE_RE = re.compile(r"^\s*(-?\d+)\s*$", re.MULTILINE)
_VOLTAGE_RE = re.compile(r"^\s*voltage\s*:\s*(-?\d+)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class EnergySettings:
    enabled: bool = False
    adb_path: str = "adb"
    command_timeout_seconds: float = 15.0
    counter_step_uah: int = 2000
    minimum_counter_ticks: int = 10


@dataclass(frozen=True)
class BatteryReading:
    timestamp: str
    monotonic_s: float
    counter_uah: int | None
    voltage_mv: int | None
    error: str | None = None


def energy_settings_from_config(cfg: dict[str, Any]) -> EnergySettings:
    raw = cfg.get("energy", {})
    if not isinstance(raw, dict):
        raise TypeError("energy config must be an object")
    settings = EnergySettings(
        enabled=bool(raw.get("enabled", False)),
        adb_path=str(raw.get("adb_path", "adb")),
        command_timeout_seconds=float(raw.get("command_timeout_seconds", 15.0)),
        counter_step_uah=int(raw.get("counter_step_uah", 2000)),
        minimum_counter_ticks=int(raw.get("minimum_counter_ticks", 10)),
    )
    if settings.command_timeout_seconds <= 0:
        raise ValueError("energy.command_timeout_seconds must be positive")
    if settings.counter_step_uah <= 0:
        raise ValueError("energy.counter_step_uah must be positive")
    if settings.minimum_counter_ticks < 1:
        raise ValueError("energy.minimum_counter_ticks must be positive")
    return settings


def new_energy_batch_id(task_group: str, performance_mode: str, physical_budget: int) -> str:
    suffix = uuid.uuid4().hex[:10]
    return f"{task_group}_{performance_mode}_b{physical_budget}_{suffix}"


def parse_counter_output(output: str) -> int | None:
    matches = _INTEGER_LINE_RE.findall(output)
    return int(matches[-1]) if matches else None


def parse_voltage_output(output: str) -> int | None:
    match = _VOLTAGE_RE.search(output)
    return int(match.group(1)) if match else None


def _run_adb(cmd: list[str], timeout_s: float) -> tuple[str, str | None]:
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return "", f"adb_error:{type(exc).__name__}"
    if completed.returncode != 0:
        detail = " ".join(completed.stderr.split())[:240].replace(";", ",")
        suffix = f":{detail}" if detail else ""
        return completed.stdout, f"adb_returncode:{completed.returncode}{suffix}"
    return completed.stdout, None


def read_battery(device: str, settings: EnergySettings) -> BatteryReading:
    if not settings.enabled:
        return BatteryReading(
            timestamp=datetime.now().astimezone().isoformat(timespec="milliseconds"),
            monotonic_s=time.monotonic(),
            counter_uah=None,
            voltage_mv=None,
            error="energy_disabled",
        )

    counter_output, counter_error = _run_adb(
        [
            settings.adb_path,
            "-s",
            device,
            "shell",
            "dumpsys",
            "battery",
            "get",
            "-f",
            "counter",
        ],
        settings.command_timeout_seconds,
    )
    # The forced counter request refreshes Health HAL state. Read voltage from
    # the immediately following full snapshot instead of forcing a second update.
    battery_output, voltage_error = _run_adb(
        [settings.adb_path, "-s", device, "shell", "dumpsys", "battery"],
        settings.command_timeout_seconds,
    )

    counter_uah = parse_counter_output(counter_output)
    voltage_mv = parse_voltage_output(battery_output)
    errors = [error for error in (counter_error, voltage_error) if error]
    if counter_uah is None:
        errors.append("counter_missing")
    if voltage_mv is None:
        errors.append("voltage_missing")
    return BatteryReading(
        timestamp=datetime.now().astimezone().isoformat(timespec="milliseconds"),
        monotonic_s=time.monotonic(),
        counter_uah=counter_uah,
        voltage_mv=voltage_mv,
        error=",".join(errors) if errors else None,
    )


def make_energy_batch_row(
    *,
    cfg: dict[str, Any],
    settings: EnergySettings,
    energy_batch_id: str,
    performance_mode: str,
    htp_performance_mode: int | None,
    htp_performance_mode_name: str,
    physical_budget_tokens: int,
    budget_execution_mode: str,
    num_physical_runs: int,
    start: BatteryReading,
    end: BatteryReading,
) -> dict[str, Any]:
    delta_uah: int | None = None
    average_voltage_mv: float | None = None
    gross_energy_j: float | None = None
    counter_ticks: float | None = None
    duration_s = max(0.0, end.monotonic_s - start.monotonic_s)
    errors = [error for error in (start.error, end.error) if error]

    if start.counter_uah is not None and end.counter_uah is not None:
        delta_uah = start.counter_uah - end.counter_uah
        if delta_uah < 0:
            errors.append("counter_increased")
    if start.voltage_mv is not None and end.voltage_mv is not None:
        average_voltage_mv = (start.voltage_mv + end.voltage_mv) / 2.0

    if delta_uah is not None and delta_uah >= 0 and average_voltage_mv is not None:
        gross_energy_j = delta_uah * average_voltage_mv * 3.6e-6
        counter_ticks = delta_uah / settings.counter_step_uah

    if errors:
        status = "read_error"
    elif delta_uah == 0:
        status = "zero_counter_delta"
    elif counter_ticks is not None and counter_ticks < settings.minimum_counter_ticks:
        status = "insufficient_counter_ticks"
    else:
        status = "ok"
    valid_for_reporting = status == "ok"

    average_power_w = (
        gross_energy_j / duration_s
        if gross_energy_j is not None and duration_s > 0
        else None
    )
    energy_per_run_j = (
        gross_energy_j / num_physical_runs
        if gross_energy_j is not None and num_physical_runs > 0
        else None
    )
    runtime = cfg["runtime"]
    notes = [
        "measurement_scope=physical_batch_endpoints",
        "energy_scope=gross_device_battery_energy",
        "voltage_aggregation=endpoint_mean",
        "raw_row_energy_j=NA",
    ]
    if start.error:
        notes.append(f"start_error={start.error}")
    if end.error:
        notes.append(f"end_error={end.error}")

    return {
        "energy_batch_id": energy_batch_id,
        "timestamp_start": start.timestamp,
        "timestamp_end": end.timestamp,
        "assignee": cfg["assignee"],
        "task_group": cfg["task_group"],
        "device_id": runtime["device"],
        "runtime": runtime["name"],
        "model": runtime["model_name"],
        "quantization": runtime["quantization"],
        "backend": runtime["backend"],
        "performance_mode": performance_mode,
        "htp_performance_mode": (
            htp_performance_mode if htp_performance_mode is not None else NA
        ),
        "htp_performance_mode_name": htp_performance_mode_name,
        "physical_budget_tokens": physical_budget_tokens,
        "budget_execution_mode": budget_execution_mode,
        "num_physical_runs": num_physical_runs,
        "start_counter_uah": start.counter_uah if start.counter_uah is not None else NA,
        "end_counter_uah": end.counter_uah if end.counter_uah is not None else NA,
        "delta_counter_uah": fmt(delta_uah),
        "start_voltage_mv": start.voltage_mv if start.voltage_mv is not None else NA,
        "end_voltage_mv": end.voltage_mv if end.voltage_mv is not None else NA,
        "average_voltage_mv": fmt(average_voltage_mv),
        "duration_s": fmt(duration_s),
        "gross_energy_j": fmt(gross_energy_j),
        "average_power_w": fmt(average_power_w),
        "energy_per_physical_run_j": fmt(energy_per_run_j),
        "counter_step_uah": settings.counter_step_uah,
        "counter_ticks": fmt(counter_ticks),
        "minimum_counter_ticks": settings.minimum_counter_ticks,
        "valid_for_reporting": fmt(valid_for_reporting),
        "measurement_status": status,
        "notes": ";".join(notes),
    }
