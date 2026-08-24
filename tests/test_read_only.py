"""Safety tests ensuring PC Guardian remains diagnostic/read-only."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = ("core", "monitors", "diagnostics", "integrations")
FORBIDDEN = (
    "SIGKILL",
    "SIGTERM",
    ".terminate(",
    ".kill(",
    "os.kill(",
    "restart_commands",
    "ActionExecutor",
)


def test_runtime_has_no_remediation_primitives() -> None:
    """Runtime modules must not contain process-remediation primitives."""
    for directory in SOURCE_DIRS:
        for path in (PROJECT_ROOT / directory).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            for token in FORBIDDEN:
                assert token not in text, f"Forbidden token {token!r} found in {path}"
