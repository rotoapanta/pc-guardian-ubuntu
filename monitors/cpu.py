"""CPU utilization and load monitor."""

from __future__ import annotations

import os

import psutil


def collect() -> dict[str, float | int]:
    """Collect CPU utilization and Linux load averages."""
    cpus = psutil.cpu_count(logical=True) or 1
    load1, load5, load15 = os.getloadavg()
    return {
        "util": round(float(psutil.cpu_percent(interval=None)), 1),
        "count": cpus,
        "load1": round(load1, 2),
        "load5": round(load5, 2),
        "load15": round(load15, 2),
        "load_per_cpu": round(load1 / cpus, 3),
    }
