"""Configuration loading utilities for PC Guardian Ubuntu."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "config.yaml"
EXAMPLE_CONFIG = PROJECT_ROOT / "config" / "config.example.yaml"


def _resolve_path(path: str | Path | None) -> Path:
    """Resolve a configuration path relative to the project root."""
    if path is None:
        return DEFAULT_CONFIG

    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    return candidate


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load YAML configuration and apply supported environment overrides.

    Args:
        path: Optional configuration path. Relative paths are resolved from
            the project root.

    Returns:
        Parsed configuration dictionary.

    Raises:
        FileNotFoundError: If neither the requested configuration nor the
            example configuration exists.
        ValueError: If the YAML root is not a mapping.
    """
    candidate = _resolve_path(path)
    if not candidate.exists():
        candidate = EXAMPLE_CONFIG

    if not candidate.exists():
        raise FileNotFoundError("No se encontró archivo de configuración.")

    with candidate.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError("La configuración YAML debe contener un mapeo raíz.")

    token = os.getenv("ZABBIX_API_TOKEN", "").strip()
    if token:
        data.setdefault("zabbix", {}).setdefault("api", {})["token"] = token

    return data
