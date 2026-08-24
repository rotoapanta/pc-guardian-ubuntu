"""Console and rotating-file logging for PC Guardian Ubuntu."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from core.config import PROJECT_ROOT

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")


def _success(self: logging.Logger, msg: str, *args: Any, **kwargs: Any) -> None:
    """Log a message using the custom SUCCESS level."""
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)


if not hasattr(logging.Logger, "success"):
    logging.Logger.success = _success


def _project_path(value: str) -> Path:
    """Return an absolute path rooted at the project directory."""
    path = Path(value).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


def setup_logger(cfg: dict[str, Any]) -> logging.Logger:
    """Create and configure the shared PC Guardian logger.

    Args:
        cfg: Complete application configuration.

    Returns:
        Configured logger instance.
    """
    logging_cfg = cfg.get("logging", {})
    logger = logging.getLogger("pcguardian")
    level_name = str(logging_cfg.get("level", "INFO")).upper()
    logger.setLevel(getattr(logging, level_name, logging.INFO))
    logger.propagate = False

    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    file_definitions = (
        ("file", logging.INFO, "logs/pc_guardian.log"),
        ("warnings_file", logging.WARNING, "logs/warnings.log"),
    )

    for key, level, default_path in file_definitions:
        path = _project_path(str(logging_cfg.get(key, default_path)))
        path.parent.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            path,
            maxBytes=int(logging_cfg.get("max_bytes", 10_485_760)),
            backupCount=int(logging_cfg.get("backup_count", 5)),
            encoding="utf-8",
        )
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
