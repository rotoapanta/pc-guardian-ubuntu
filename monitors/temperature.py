"""CPU and NVMe temperature monitor."""

from __future__ import annotations

from typing import Any

import psutil


def collect() -> dict[str, Any]:
    """Collect maximum CPU and NVMe temperatures in degrees Celsius."""
    try:
        groups = psutil.sensors_temperatures(fahrenheit=False) or {}
    except (AttributeError, OSError, RuntimeError):
        groups = {}

    readings: list[dict[str, str | float]] = []
    cpu_values: list[float] = []
    nvme_values: list[float] = []

    for sensor, entries in groups.items():
        for index, entry in enumerate(entries):
            if entry.current is None:
                continue
            value = round(float(entry.current), 1)
            readings.append(
                {
                    "sensor": sensor,
                    "label": entry.label or f"sensor-{index}",
                    "current": value,
                }
            )
            sensor_name = sensor.lower()
            if "coretemp" in sensor_name or "cpu" in sensor_name:
                cpu_values.append(value)
            if "nvme" in sensor_name:
                nvme_values.append(value)

    return {
        "cpu_max": max(cpu_values, default=0.0),
        "nvme_max": max(nvme_values, default=0.0),
        "readings": readings,
    }
