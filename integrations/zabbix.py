"""Zabbix Sender integration for PC Guardian Ubuntu.

Telemetry is exported as Zabbix trapper metrics. Physical quantities use
base units where practical so Zabbix performs automatic display scaling.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any


def key_component(name: str) -> str:
    """Convert a process name into a safe dot-separated key component."""
    clean = re.sub(r"[^a-z0-9]+", ".", name.lower()).strip(".")
    return clean or "unknown"


def build_metrics(
    snapshot: dict[str, Any],
    watchlist: list[str],
) -> dict[str, float | int]:
    """Convert a telemetry snapshot into Zabbix item-key/value pairs."""
    metrics: dict[str, float | int] = {
        "pcguardian.status": 1,
        "pcguardian.cpu.util": snapshot["cpu"]["util"],
        "pcguardian.cpu.load.1m": snapshot["cpu"]["load1"],
        "pcguardian.cpu.load.5m": snapshot["cpu"]["load5"],
        "pcguardian.cpu.load.percpu": snapshot["cpu"]["load_per_cpu"],
        "pcguardian.cpu.temperature": snapshot["temperature"]["cpu_max"],
        "pcguardian.nvme.temperature": snapshot["temperature"]["nvme_max"],
        "pcguardian.memory.util": snapshot["memory"]["util"],
        "pcguardian.memory.available": snapshot["memory"]["available_bytes"],
        "pcguardian.swap.util": snapshot["memory"]["swap_util"],
        "pcguardian.disk.root.util": snapshot["disk"]["root_util"],
        "pcguardian.disk.root.free": snapshot["disk"]["root_free_bytes"],
        "pcguardian.disk.read": snapshot["disk"]["read_bytes_per_second"],
        "pcguardian.disk.write": snapshot["disk"]["write_bytes_per_second"],
        "pcguardian.psi.cpu.avg10": snapshot["psi"]["cpu"],
        "pcguardian.psi.memory.avg10": snapshot["psi"]["memory"],
        "pcguardian.psi.io.avg10": snapshot["psi"]["io"],
        "pcguardian.process.count": snapshot["process"]["count"],
        "pcguardian.process.dstate.count": snapshot["process"]["d_count"],
        "pcguardian.process.i915.dstate.count": snapshot["process"]["i915_d_count"],
    }

    watched = snapshot["process"]["watchlist"]
    for name in watchlist:
        component = key_component(name)
        process = watched.get(name, {"cpu": 0, "memory": 0, "instances": 0})
        metrics[f"pcguardian.process.{component}.cpu"] = process["cpu"]
        metrics[f"pcguardian.process.{component}.memory"] = process["memory"]
        metrics[f"pcguardian.process.{component}.instances"] = process["instances"]

    return metrics


class ZabbixSender:
    """Send metric batches to Zabbix Server using ``zabbix_sender``."""

    def __init__(self, cfg: dict[str, Any], logger: Any) -> None:
        """Initialize sender state from application configuration."""
        self.cfg = cfg.get("zabbix", {})
        self.logger = logger
        self.last_send = 0.0
        self.last_ok: bool | None = None

    def due(self) -> bool:
        """Return whether a new Zabbix transmission is due."""
        interval = float(self.cfg.get("send_interval_seconds", 10))
        enabled = bool(self.cfg.get("enabled", False))
        return enabled and time.monotonic() - self.last_send >= interval

    def send(self, metrics: dict[str, float | int]) -> bool:
        """Send one metric batch and return whether Zabbix accepted all values."""
        self.last_send = time.monotonic()
        sender_binary = Path(str(self.cfg.get("sender_binary", "/usr/bin/zabbix_sender")))

        if not sender_binary.exists():
            self.logger.error("zabbix_sender no encontrado: %s", sender_binary)
            self.last_ok = False
            return False

        host = str(self.cfg.get("host", "")).strip()
        if not host:
            self.logger.error("No se ha configurado zabbix.host")
            self.last_ok = False
            return False

        lines = [f'"{host}" {key} {value}' for key, value in metrics.items()]
        temporary_path: Path | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                prefix="pcguardian_",
                suffix=".zbx",
                delete=False,
            ) as handle:
                handle.write("\n".join(lines) + "\n")
                temporary_path = Path(handle.name)

            server = str(self.cfg.get("server", "127.0.0.1"))
            port = int(self.cfg.get("port", 10051))
            self.logger.info("Enviando %d métricas a Zabbix %s:%d", len(metrics), server, port)

            result = subprocess.run(
                [str(sender_binary), "-z", server, "-p", str(port), "-i", str(temporary_path)],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            output = ((result.stdout or "") + (result.stderr or "")).strip()
            success = result.returncode == 0 and "failed: 0" in output
            self.last_ok = success

            if success:
                self.logger.success("Métricas enviadas correctamente a Zabbix")
                self.logger.debug("Respuesta zabbix_sender: %s", output)
            else:
                self.logger.warning("Error enviando a Zabbix: %s", output)
            return success

        except subprocess.TimeoutExpired:
            self.last_ok = False
            self.logger.error("Timeout enviando métricas a Zabbix")
            return False
        except OSError:
            self.last_ok = False
            self.logger.exception("Error ejecutando zabbix_sender")
            return False
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    self.logger.warning("No se pudo eliminar archivo temporal: %s", temporary_path)
