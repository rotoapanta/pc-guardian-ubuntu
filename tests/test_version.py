"""Version consistency tests."""

from pathlib import Path

from core.version import __version__

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_version_file_matches_python_version() -> None:
    """VERSION and the Python runtime version must remain synchronized."""
    assert (PROJECT_ROOT / "VERSION").read_text(encoding="utf-8").strip() == __version__
