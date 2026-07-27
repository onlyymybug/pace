from __future__ import annotations

import math
import re
import statistics
import subprocess
import time
from dataclasses import dataclass
from typing import Any

from .constants import NA
from .metrics import fmt


_STATUS_RE = re.compile(r"^Thermal Status:\s*(-?\d+)\s*$", re.MULTILINE)
_TEMPERATURE_RE = re.compile(
    r"Temperature\{mValue=([^,]+),\s*mType=(-?\d+),\s*"
    r"mName=([^,}]+),\s*mStatus=(-?\d+)\}"
)


@dataclass(frozen=True)
class ThermalSettings:
    enabled: bool = False
    adb_path: str = "adb"
    baseline_temp_c: float | None = None
    command_timeout_seconds: float = 10.0
    poll_interval_seconds: float = 10.0
    stable_samples: int = 4
    stability_range_c: float = 0.5
    baseline_tolerance_c: float = 0.5
    cooldown_timeout_seconds: float = 900.0
    max_consecutive_read_failures: int = 3


@dataclass(frozen=True)
class ThermalReading:
    skin_temp_c: float | None
    npu_temp_c: float | None
    thermal_status: int | None
    error: str | None = None


def thermal_settings_from_config(cfg: dict[str, Any]) -> ThermalSettings:
    raw = cfg.get("thermal", {})
    if not isinstance(raw, dict):
        raise TypeError("thermal config must be an object")
    baseline_value = raw.get("baseline_temp_c")
    baseline_temp_c = None if baseline_value is None else float(baseline_value)
    settings = ThermalSettings(
        enabled=bool(raw.get("enabled", False)),
        adb_path=str(raw.get("adb_path", "adb")),
        baseline_temp_c=baseline_temp_c,
        command_timeout_seconds=float(raw.get("command_timeout_seconds", 10.0)),
        poll_interval_seconds=float(raw.get("poll_interval_seconds", 10.0)),
        stable_samples=int(raw.get("stable_samples", 4)),
        stability_range_c=float(raw.get("stability_range_c", 0.5)),
        baseline_tolerance_c=float(raw.get("baseline_tolerance_c", 0.5)),
        cooldown_timeout_seconds=float(raw.get("cooldown_timeout_seconds", 900.0)),
        max_consecutive_read_failures=int(raw.get("max_consecutive_read_failures", 3)),
    )
    if settings.stable_samples < 2:
        raise ValueError("thermal.stable_samples must be at least 2")
    if settings.poll_interval_seconds <= 0:
        raise ValueError("thermal.poll_interval_seconds must be positive")
    if settings.cooldown_timeout_seconds <= 0:
        raise ValueError("thermal.cooldown_timeout_seconds must be positive")
    if settings.stability_range_c < 0 or settings.baseline_tolerance_c < 0:
        raise ValueError("thermal temperature tolerances must be non-negative")
    if settings.max_consecutive_read_failures < 1:
        raise ValueError("thermal.max_consecutive_read_failures must be positive")
    if settings.baseline_temp_c is not None and not math.isfinite(
        settings.baseline_temp_c
    ):
        raise ValueError("thermal.baseline_temp_c must be a finite number or null")
    return settings


def parse_thermalservice_output(output: str) -> ThermalReading:
    status_match = _STATUS_RE.search(output)
    thermal_status = int(status_match.group(1)) if status_match else None

    section_marker = "Current temperatures from HAL:"
    if section_marker not in output:
        return ThermalReading(None, None, thermal_status, "current_hal_section_missing")

    current_section = output.split(section_marker, 1)[1]
    current_section = current_section.split("Current cooling devices from HAL:", 1)[0]

    skin_values: list[float] = []
    npu_values: list[float] = []
    for match in _TEMPERATURE_RE.finditer(current_section):
        try:
            value = float(match.group(1))
            sensor_type = int(match.group(2))
        except ValueError:
            continue
        if not math.isfinite(value) or value <= -100.0:
            continue
        name = match.group(3).strip()
        if sensor_type == 3 and name == "skin":
            skin_values.append(value)
        elif sensor_type == 9:
            npu_values.append(value)

    errors: list[str] = []
    if not skin_values:
        errors.append("skin_missing")
    if not npu_values:
        errors.append("npu_missing")
    if thermal_status is None:
        errors.append("thermal_status_missing")
    return ThermalReading(
        skin_temp_c=skin_values[0] if skin_values else None,
        npu_temp_c=max(npu_values) if npu_values else None,
        thermal_status=thermal_status,
        error=",".join(errors) if errors else None,
    )


def read_thermal(device: str, settings: ThermalSettings) -> ThermalReading:
    if not settings.enabled:
        return ThermalReading(None, None, None, "thermal_disabled")
    cmd = [
        settings.adb_path,
        "-s",
        device,
        "shell",
        "dumpsys",
        "thermalservice",
    ]
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=settings.command_timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return ThermalReading(None, None, None, f"adb_error:{type(exc).__name__}")
    if completed.returncode != 0:
        return ThermalReading(
            None,
            None,
            None,
            f"adb_returncode:{completed.returncode}",
        )
    return parse_thermalservice_output(completed.stdout)


def thermal_pair_fields(
    start: ThermalReading,
    end: ThermalReading,
) -> dict[str, Any]:
    statuses = [x for x in (start.thermal_status, end.thermal_status) if x is not None]
    return {
        "start_temp_c": fmt(start.skin_temp_c),
        "end_temp_c": fmt(end.skin_temp_c),
        "start_npu_temp_c": fmt(start.npu_temp_c),
        "end_npu_temp_c": fmt(end.npu_temp_c),
        "thermal_status": max(statuses) if statuses else NA,
    }


def thermal_pair_notes(
    start: ThermalReading,
    end: ThermalReading,
    common_skin_baseline_c: float | None = None,
) -> list[str]:
    notes = [
        # "temp_sensor=android_thermal_hal:skin",
        # "npu_temp_sensor=max(android_thermal_hal:type9)",
        # "thermal_measurement_scope=physical_runner_endpoints",
        # "thermal_status_aggregation=max_endpoints",
        # f"common_skin_baseline_c={fmt(common_skin_baseline_c)}",
        # f"thermal_status_start={start.thermal_status if start.thermal_status is not None else NA}",
        # f"thermal_status_end={end.thermal_status if end.thermal_status is not None else NA}",
    ]
    if start.error:
        notes.append(f"thermal_start_error={start.error}")
    if end.error:
        notes.append(f"thermal_end_error={end.error}")
    return notes


def wait_for_skin_baseline(
    *,
    device: str,
    settings: ThermalSettings,
    performance_mode: str,
    target_baseline_c: float | None,
) -> float:
    if not settings.enabled:
        return float("nan")

    action = "establishing" if target_baseline_c is None else "returning to"
    target_text = "stable idle skin" if target_baseline_c is None else f"{target_baseline_c:.3f} C"
    print(f"[thermal] {action} baseline before {performance_mode}: {target_text}")

    deadline = time.monotonic() + settings.cooldown_timeout_seconds
    temperatures: list[float] = []
    consecutive_failures = 0
    while time.monotonic() <= deadline:
        reading = read_thermal(device, settings)
        if reading.skin_temp_c is None:
            consecutive_failures += 1
            print(f"[thermal] baseline read failed: {reading.error or 'skin_missing'}")
            if consecutive_failures >= settings.max_consecutive_read_failures:
                raise RuntimeError("Unable to read HAL skin temperature during cooldown")
        else:
            consecutive_failures = 0
            temperatures.append(reading.skin_temp_c)
            temperatures = temperatures[-settings.stable_samples :]
            observed_range = max(temperatures) - min(temperatures)
            window_mean = statistics.mean(temperatures)
            target_ok = target_baseline_c is None or (
                abs(window_mean - target_baseline_c) <= settings.baseline_tolerance_c
            )
            print(
                f"[thermal] skin={reading.skin_temp_c:.3f} C "
                f"window={len(temperatures)}/{settings.stable_samples}"
            )
            if (
                len(temperatures) == settings.stable_samples
                and observed_range <= settings.stability_range_c
                and target_ok
            ):
                baseline = window_mean
                print(
                    f"[thermal] baseline ready before {performance_mode}: "
                    f"mean={baseline:.3f} C range={observed_range:.3f} C"
                )
                return baseline if target_baseline_c is None else target_baseline_c

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        time.sleep(min(settings.poll_interval_seconds, remaining))

    raise TimeoutError(
        f"Skin temperature did not return to the common baseline before {performance_mode} "
        f"within {settings.cooldown_timeout_seconds:.0f} seconds"
    )
