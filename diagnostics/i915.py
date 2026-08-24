"""Intel i915/DRM kernel-log diagnostic helper."""

from __future__ import annotations

import subprocess


def read_kernel_log() -> str:
    """Return recent kernel messages related to Intel graphics/DRM."""
    command = [
        "journalctl",
        "-k",
        "-b",
        "--no-pager",
    ]
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

    keywords = ("i915", "drm", "gpu", "hang", "reset", "flip", "atomic", "fence")
    lines = [
        line
        for line in result.stdout.splitlines()
        if any(keyword in line.lower() for keyword in keywords)
    ]
    return "\n".join(lines[-200:])
