"""Linux Pressure Stall Information (PSI) monitor."""

from __future__ import annotations

from pathlib import Path

PRESSURE_ROOT = Path("/proc/pressure")


def _avg10(resource: str) -> float:
    """Return the ``some avg10`` percentage for a PSI resource."""
    path = PRESSURE_ROOT / resource
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return 0.0

    if not lines:
        return 0.0

    for token in lines[0].split():
        if token.startswith("avg10="):
            try:
                return float(token.split("=", 1)[1])
            except ValueError:
                return 0.0
    return 0.0


def collect() -> dict[str, float]:
    """Collect CPU, memory, and I/O PSI ``some avg10`` percentages."""
    return {
        "cpu": _avg10("cpu"),
        "memory": _avg10("memory"),
        "io": _avg10("io"),
    }
