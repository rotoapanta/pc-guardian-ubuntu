"""Zabbix metric mapping tests."""

from integrations.zabbix import build_metrics


def _snapshot() -> dict:
    """Return a deterministic telemetry snapshot for Zabbix tests."""
    return {
        "cpu": {"util": 10, "load1": 1, "load5": 1, "load_per_cpu": 0.1},
        "temperature": {"cpu_max": 55, "nvme_max": 50},
        "memory": {
            "util": 40,
            "available_bytes": 8 * 1024**3,
            "available_mb": 8192,
            "swap_util": 0,
        },
        "disk": {
            "root_util": 80,
            "root_free_bytes": 170 * 1024**3,
            "read_bytes_per_second": 1024,
            "write_bytes_per_second": 2048,
        },
        "psi": {"cpu": 0, "memory": 0, "io": 0},
        "process": {
            "count": 300,
            "d_count": 0,
            "i915_d_count": 0,
            "watchlist": {
                "snapd": {"cpu": 0, "memory": 0, "instances": 1},
                "firefox": {"cpu": 1, "memory": 2, "instances": 3},
                "gnome-shell": {"cpu": 1, "memory": 1, "instances": 1},
                "Xorg": {"cpu": 1, "memory": 1, "instances": 1},
            },
        },
    }


def test_dot_keys_only() -> None:
    """All metric keys use the agreed dot-separated convention."""
    metrics = build_metrics(_snapshot(), ["snapd"])
    assert "pcguardian.memory.available" in metrics
    assert "pcguardian.disk.root.free" in metrics
    assert "pcguardian.process.snapd.cpu" in metrics
    assert all("[" not in key and "]" not in key for key in metrics)


def test_default_watchlist_produces_32_metrics() -> None:
    """Four watched processes produce the expected 32 metrics."""
    watchlist = ["snapd", "firefox", "gnome-shell", "Xorg"]
    metrics = build_metrics(_snapshot(), watchlist)
    assert len(metrics) == 32
