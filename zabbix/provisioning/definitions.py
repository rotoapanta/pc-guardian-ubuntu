"""Zabbix item and trigger definitions for Ubuntu Desktop monitoring.

This module contains the reusable item and trigger definitions used by
the Zabbix provisioning system.

Physical quantities use base units whenever possible so Zabbix can
perform automatic unit scaling.

Trigger descriptions and expressions use the ``{TEMPLATE}`` placeholder.
The provisioning layer replaces it dynamically with the template name
configured in ``config/config.yaml``.
"""

from __future__ import annotations

BASE_ITEMS: list[tuple[str, str, int, str]] = [
    (
        "PC Guardian status",
        "pcguardian.status",
        3,
        "",
    ),
    (
        "CPU utilization",
        "pcguardian.cpu.util",
        0,
        "%",
    ),
    (
        "CPU load 1m",
        "pcguardian.cpu.load.1m",
        0,
        "",
    ),
    (
        "CPU load 5m",
        "pcguardian.cpu.load.5m",
        0,
        "",
    ),
    (
        "CPU load per CPU",
        "pcguardian.cpu.load.percpu",
        0,
        "",
    ),
    (
        "CPU temperature",
        "pcguardian.cpu.temperature",
        0,
        "°C",
    ),
    (
        "NVMe temperature",
        "pcguardian.nvme.temperature",
        0,
        "°C",
    ),
    (
        "Memory utilization",
        "pcguardian.memory.util",
        0,
        "%",
    ),
    (
        "Available memory",
        "pcguardian.memory.available",
        3,
        "B",
    ),
    (
        "Swap utilization",
        "pcguardian.swap.util",
        0,
        "%",
    ),
    (
        "Root disk utilization",
        "pcguardian.disk.root.util",
        0,
        "%",
    ),
    (
        "Root disk free",
        "pcguardian.disk.root.free",
        3,
        "B",
    ),
    (
        "Disk read",
        "pcguardian.disk.read",
        0,
        "Bps",
    ),
    (
        "Disk write",
        "pcguardian.disk.write",
        0,
        "Bps",
    ),
    (
        "PSI CPU avg10",
        "pcguardian.psi.cpu.avg10",
        0,
        "%",
    ),
    (
        "PSI memory avg10",
        "pcguardian.psi.memory.avg10",
        0,
        "%",
    ),
    (
        "PSI IO avg10",
        "pcguardian.psi.io.avg10",
        0,
        "%",
    ),
    (
        "Process count",
        "pcguardian.process.count",
        3,
        "",
    ),
    (
        "D-state process count",
        "pcguardian.process.dstate.count",
        3,
        "",
    ),
    (
        "i915 D-state process count",
        "pcguardian.process.i915.dstate.count",
        3,
        "",
    ),
]


TRIGGERS: list[tuple[str, str, int]] = [
    (
        "{TEMPLATE}: no data for 2 minutes",
        "nodata(/{TEMPLATE}/pcguardian.status,2m)=1",
        4,
    ),
    (
        "{TEMPLATE}: CPU >95% for 5m",
        "min(/{TEMPLATE}/pcguardian.cpu.util,5m)>95",
        4,
    ),
    (
        "{TEMPLATE}: CPU temperature >85C for 5m",
        "min(/{TEMPLATE}/pcguardian.cpu.temperature,5m)>85",
        4,
    ),
    (
        "{TEMPLATE}: CPU temperature >92C for 2m",
        "min(/{TEMPLATE}/pcguardian.cpu.temperature,2m)>92",
        5,
    ),
    (
        "{TEMPLATE}: NVMe temperature >75C for 5m",
        "min(/{TEMPLATE}/pcguardian.nvme.temperature,5m)>75",
        4,
    ),
    (
        "{TEMPLATE}: root disk >90%",
        "min(/{TEMPLATE}/pcguardian.disk.root.util,5m)>90",
        2,
    ),
    (
        "{TEMPLATE}: root disk >95%",
        "min(/{TEMPLATE}/pcguardian.disk.root.util,5m)>95",
        4,
    ),
    (
        "{TEMPLATE}: memory pressure high",
        (
            "min(/{TEMPLATE}/pcguardian.memory.util,5m)>90"
            " and "
            "min(/{TEMPLATE}/pcguardian.psi.memory.avg10,5m)>10"
        ),
        4,
    ),
    (
        "{TEMPLATE}: swap high with memory pressure",
        (
            "min(/{TEMPLATE}/pcguardian.swap.util,5m)>90"
            " and "
            "min(/{TEMPLATE}/pcguardian.psi.memory.avg10,5m)>10"
        ),
        2,
    ),
    (
        "{TEMPLATE}: IO pressure high",
        "min(/{TEMPLATE}/pcguardian.psi.io.avg10,5m)>25",
        4,
    ),
    (
        "{TEMPLATE}: D-state processes persist",
        "min(/{TEMPLATE}/pcguardian.process.dstate.count,2m)>=2",
        4,
    ),
    (
        "{TEMPLATE}: i915 D-state persists",
        "min(/{TEMPLATE}/pcguardian.process.i915.dstate.count,2m)>=1",
        2,
    ),
]


LEGACY_TRIGGER_NAMES: dict[str, str] = {
    "PC Guardian: no data for 2 minutes": "{TEMPLATE}: no data for 2 minutes",
    "PC Guardian: CPU >95% for 5m": "{TEMPLATE}: CPU >95% for 5m",
    "PC Guardian: CPU temperature >85C for 5m": "{TEMPLATE}: CPU temperature >85C for 5m",
    "PC Guardian: CPU temperature >92C for 2m": "{TEMPLATE}: CPU temperature >92C for 2m",
    "PC Guardian: NVMe temperature >75C for 5m": "{TEMPLATE}: NVMe temperature >75C for 5m",
    "PC Guardian: root disk >90%": "{TEMPLATE}: root disk >90%",
    "PC Guardian: root disk >95%": "{TEMPLATE}: root disk >95%",
    "PC Guardian: swap >80% for 10m": "{TEMPLATE}: swap high with memory pressure",
    "PC Guardian: memory pressure high": "{TEMPLATE}: memory pressure high",
    "PC Guardian: IO pressure high": "{TEMPLATE}: IO pressure high",
    "PC Guardian: D-state processes persist": "{TEMPLATE}: D-state processes persist",
    "PC Guardian: i915 D-state persists": "{TEMPLATE}: i915 D-state persists",
}
