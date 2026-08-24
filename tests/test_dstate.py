"""D-state process summary tests."""

from monitors.processes import summarize


def test_dstate_count() -> None:
    """Disk-sleep processes are counted as D-state."""
    rows = [
        {
            "pid": 10,
            "name": "kworker/test+i915_flip",
            "command": "",
            "status": "disk-sleep",
            "cpu": 0,
            "memory": 0,
        }
    ]
    data = summarize(rows, [])
    assert data["d_count"] == 1
    assert data["i915_d_count"] == 1
