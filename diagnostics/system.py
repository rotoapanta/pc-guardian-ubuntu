"""Threshold-based system diagnostics for PC Guardian Ubuntu.

Swap occupancy alone is not treated as a fault. High swap is reported only
when active memory PSI also indicates pressure, reducing false positives on
Linux systems that retain cold pages in swap.
"""

from __future__ import annotations

from typing import Any


def evaluate(snapshot: dict[str, Any], cfg: dict[str, Any]) -> list[str]:
    """Return currently active diagnostic conditions."""
    limits = cfg.get("limits", {})
    reasons: list[str] = []

    cpu_util = float(snapshot["cpu"]["util"])
    memory_util = float(snapshot["memory"]["util"])
    available_mb = float(snapshot["memory"]["available_mb"])
    swap_util = float(snapshot["memory"]["swap_util"])
    disk_util = float(snapshot["disk"]["root_util"])
    cpu_temp = float(snapshot["temperature"]["cpu_max"])
    nvme_temp = float(snapshot["temperature"]["nvme_max"])
    load_per_cpu = float(snapshot["cpu"]["load_per_cpu"])
    psi_cpu = float(snapshot["psi"]["cpu"])
    psi_memory = float(snapshot["psi"]["memory"])
    psi_io = float(snapshot["psi"]["io"])
    d_count = int(snapshot["process"]["d_count"])
    i915_count = int(snapshot["process"]["i915_d_count"])

    if cpu_util >= float(limits.get("cpu_percent", 95)):
        reasons.append(f"CPU {cpu_util}%")
    if memory_util >= float(limits.get("memory_percent", 92)):
        reasons.append(f"RAM {memory_util}%")
    if available_mb <= float(limits.get("memory_available_mb", 700)):
        reasons.append(f"RAM disponible baja ({available_mb:.0f} MiB)")

    swap_threshold = float(limits.get("swap_percent", 90))
    psi_memory_threshold = float(limits.get("psi_memory_avg10", 10))
    if swap_util >= swap_threshold and psi_memory >= psi_memory_threshold:
        reasons.append(
            f"Swap alto con presión de memoria (swap={swap_util}% | psi_memory={psi_memory}%)"
        )

    if disk_util >= float(limits.get("disk_percent", 90)):
        reasons.append(f"Disco raíz {disk_util}%")
    if cpu_temp >= float(limits.get("cpu_temperature_c", 85)):
        reasons.append(f"Temperatura CPU {cpu_temp}°C")
    if nvme_temp >= float(limits.get("nvme_temperature_c", 75)):
        reasons.append(f"Temperatura NVMe {nvme_temp}°C")
    if load_per_cpu >= float(limits.get("load_per_cpu", 1.5)):
        reasons.append(f"Load/CPU {load_per_cpu}")
    if psi_cpu >= float(limits.get("psi_cpu_avg10", 50)):
        reasons.append(f"PSI CPU {psi_cpu}%")
    if psi_memory >= psi_memory_threshold:
        reasons.append(f"PSI memory {psi_memory}%")
    if psi_io >= float(limits.get("psi_io_avg10", 25)):
        reasons.append(f"PSI IO {psi_io}%")
    if d_count >= int(limits.get("d_state_count", 2)):
        reasons.append(f"D-state {d_count}")
    if i915_count >= int(limits.get("i915_d_state_count", 1)):
        reasons.append(f"i915 D-state {i915_count}")

    return reasons
