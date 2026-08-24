"""Process inventory and D-state monitoring."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import psutil

MIB = 1024**2


def _wchan(pid: int) -> str:
    """Read the Linux wait channel for a process."""
    try:
        return Path(f"/proc/{pid}/wchan").read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def collect() -> list[dict[str, Any]]:
    """Collect a sortable process table for diagnostics and watchlists."""
    rows: list[dict[str, Any]] = []
    attrs = [
        "pid",
        "ppid",
        "name",
        "username",
        "memory_percent",
        "status",
        "cmdline",
        "num_threads",
    ]

    for process in psutil.process_iter(attrs):
        try:
            info = process.info
            rows.append(
                {
                    "pid": info["pid"],
                    "ppid": info.get("ppid") or 0,
                    "name": info.get("name") or "unknown",
                    "username": info.get("username") or "",
                    "cpu": round(process.cpu_percent(interval=None), 1),
                    "memory": round(float(info.get("memory_percent") or 0), 2),
                    "memory_mb": round(process.memory_info().rss / MIB, 1),
                    "status": info.get("status") or "unknown",
                    "threads": info.get("num_threads") or 0,
                    "command": " ".join(info.get("cmdline") or []),
                    "wchan": _wchan(info["pid"]),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return sorted(rows, key=lambda row: (row["cpu"], row["memory"]), reverse=True)


def summarize(rows: list[dict[str, Any]], watchlist: list[str]) -> dict[str, Any]:
    """Build D-state counters and per-process watchlist metrics."""
    d_state = [row for row in rows if row["status"] == psutil.STATUS_DISK_SLEEP]
    i915 = [row for row in d_state if "i915" in f"{row['name']} {row['command']}".lower()]

    watched: dict[str, dict[str, float | int]] = {}
    for name in watchlist:
        members = [row for row in rows if row["name"].lower() == name.lower()]
        watched[name] = {
            "cpu": round(sum(float(row["cpu"]) for row in members), 2),
            "memory": round(sum(float(row["memory"]) for row in members), 2),
            "instances": len(members),
        }

    return {
        "count": len(rows),
        "d_count": len(d_state),
        "i915_d_count": len(i915),
        "d_processes": d_state,
        "watchlist": watched,
    }
