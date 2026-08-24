"""Helpers for collecting Linux D-state forensic evidence."""

from __future__ import annotations

from pathlib import Path


def read_stack(pid: int) -> str:
    """Read ``/proc/PID/stack`` when permissions allow it."""
    try:
        return Path(f"/proc/{pid}/stack").read_text(encoding="utf-8")
    except OSError as exc:
        return f"unavailable: {exc}"
