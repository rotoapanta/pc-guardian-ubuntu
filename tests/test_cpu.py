"""CPU monitor tests."""

from monitors import cpu


def test_cpu_collect_keys() -> None:
    """CPU collector exposes utilization and normalized load."""
    data = cpu.collect()
    assert "util" in data
    assert "load_per_cpu" in data
    assert int(data["count"]) >= 1
