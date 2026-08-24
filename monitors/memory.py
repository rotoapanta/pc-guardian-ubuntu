"""RAM and swap monitor.

Capacity values are kept in bytes for Zabbix automatic unit scaling. A
MiB compatibility value is also exposed for local diagnostic thresholds.
"""

from __future__ import annotations

import psutil

MIB = 1024**2


def collect() -> dict[str, float | int]:
    """Collect RAM utilization, available memory, and swap utilization."""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "util": round(float(memory.percent), 1),
        "available_bytes": int(memory.available),
        "available_mb": round(memory.available / MIB, 1),
        "swap_util": round(float(swap.percent), 1),
    }
