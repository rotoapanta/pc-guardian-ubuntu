"""Root filesystem and disk I/O monitor.

Filesystem capacity is reported in bytes and throughput in bytes per
second so Zabbix can scale the values automatically.
"""

from __future__ import annotations

import time

import psutil


class DiskMonitor:
    """Collect root filesystem usage and aggregate disk I/O throughput."""

    def __init__(self) -> None:
        """Initialize rate-calculation state."""
        self.previous_io: tuple[int, int] | None = None
        self.previous_time = time.monotonic()

    def collect(self) -> dict[str, float | int]:
        """Collect root usage, free bytes, and read/write throughput."""
        usage = psutil.disk_usage("/")
        io = psutil.disk_io_counters()
        now = time.monotonic()
        current_io = (io.read_bytes if io else 0, io.write_bytes if io else 0)

        read_bps = 0.0
        write_bps = 0.0
        if self.previous_io is not None:
            elapsed = max(now - self.previous_time, 0.001)
            read_bps = max(current_io[0] - self.previous_io[0], 0) / elapsed
            write_bps = max(current_io[1] - self.previous_io[1], 0) / elapsed

        self.previous_io = current_io
        self.previous_time = now
        return {
            "root_util": round(float(usage.percent), 1),
            "root_free_bytes": int(usage.free),
            "read_bytes_per_second": round(read_bps, 2),
            "write_bytes_per_second": round(write_bps, 2),
        }
