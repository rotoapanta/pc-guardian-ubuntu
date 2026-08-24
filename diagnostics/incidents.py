"""Forensic incident evidence writer."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from core.config import PROJECT_ROOT
from diagnostics.dstate import read_stack
from diagnostics.i915 import read_kernel_log


def _run(command: list[str]) -> str:
    """Run a read-only diagnostic command and return combined output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable: {exc}"
    return ((result.stdout or "") + (result.stderr or "")).strip()


def capture(
    directory: str,
    reason: str,
    snapshot: dict[str, Any],
    processes: list[dict[str, Any]],
) -> str:
    """Create a JSON forensic report for a sustained diagnostic event."""
    target = Path(directory).expanduser()
    if not target.is_absolute():
        target = PROJECT_ROOT / target
    target.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    report = target / f"incident_{stamp}.json"

    d_state: list[dict[str, Any]] = []
    for process in processes:
        if process.get("status") == "disk-sleep":
            row = dict(process)
            row["stack"] = read_stack(int(process["pid"]))
            d_state.append(row)

    payload = {
        "created_at": datetime.now().astimezone().isoformat(),
        "reason": reason,
        "snapshot": snapshot,
        "top_processes": processes[:30],
        "d_state_processes": d_state,
        "i915_drm_log": read_kernel_log(),
        "kernel_warnings": _run(
            [
                "journalctl",
                "-k",
                "-b",
                "-p",
                "warning..alert",
                "--no-pager",
                "-n",
                "200",
            ]
        ),
    }

    report.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return str(report)
