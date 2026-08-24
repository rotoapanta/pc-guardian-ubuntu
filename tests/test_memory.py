"""Memory monitor tests."""

from monitors import memory


def test_memory_collect_keys() -> None:
    """Memory collector exposes base-unit and diagnostic values."""
    data = memory.collect()
    assert "util" in data
    assert "available_bytes" in data
    assert "available_mb" in data
    assert "swap_util" in data
    assert int(data["available_bytes"]) >= 0
