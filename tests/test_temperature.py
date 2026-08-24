"""Temperature monitor tests."""

from monitors import temperature


def test_temperature_collect_shape() -> None:
    """Temperature collector always returns the documented shape."""
    data = temperature.collect()
    assert "cpu_max" in data
    assert "nvme_max" in data
    assert "readings" in data
