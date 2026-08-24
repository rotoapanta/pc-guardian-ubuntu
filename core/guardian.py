"""Main monitoring orchestrator for PC Guardian Ubuntu.

PC Guardian is intentionally read-only with respect to process and system
state. It collects telemetry, evaluates diagnostic conditions, preserves
incident evidence, and exports metrics to Zabbix. It never terminates,
restarts, renices, or otherwise remediates processes.
"""

from __future__ import annotations

import platform
import time
from datetime import datetime
from typing import Any

from core.version import __version__
from diagnostics.incidents import capture
from diagnostics.system import evaluate
from integrations.zabbix import ZabbixSender, build_metrics
from monitors import cpu, memory, processes, psi, temperature
from monitors.disk import DiskMonitor


class PCGuardian:
    """Coordinate telemetry collection, diagnostics, and Zabbix export."""
    def __init__(self, cfg: dict[str, Any], logger: Any) -> None:
        """Initialize the monitoring components."""
        self.cfg = cfg
        self.logger = logger
        self.disk = DiskMonitor()
        self.zabbix = ZabbixSender(cfg, logger)
        self.last_summary = 0.0
        self.last_incident = 0.0
        self.violation_counts: dict[str, int] = {}

    def collect_snapshot(self) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        """Collect a complete system snapshot and raw process table."""
        process_rows = processes.collect()
        snapshot: dict[str, Any] = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "cpu": cpu.collect(),
            "memory": memory.collect(),
            "disk": self.disk.collect(),
            "temperature": temperature.collect(),
            "psi": psi.collect(),
            "process": processes.summarize(
                process_rows,
                self.cfg.get("watchlist", []),
            ),
        }
        return snapshot, process_rows

    def _sustained(self, reasons: list[str]) -> list[str]:
        """Return diagnostic conditions sustained for enough samples."""
        active = set(reasons)
        known_conditions = set(self.violation_counts) | active

        for condition in known_conditions:
            if condition in active:
                self.violation_counts[condition] = self.violation_counts.get(condition, 0) + 1
            else:
                self.violation_counts[condition] = 0

        required_samples = int(self.cfg.get("limits", {}).get("consecutive_samples", 5))
        return [
            condition
            for condition, count in self.violation_counts.items()
            if count >= required_samples
        ]

    def _zabbix_state(self) -> str:
        """Return OFF, PENDING, OK, or ERROR for the Zabbix sender."""
        if not self.cfg.get("zabbix", {}).get("enabled", False):
            return "OFF"
        if self.zabbix.last_ok is None:
            return "PENDING"
        return "OK" if self.zabbix.last_ok else "ERROR"

    def _summary(self, snapshot: dict[str, Any]) -> None:
        """Write a compact telemetry summary to the application logger."""
        self.logger.info(
            "CPU %.1f%% | RAM %.1f%% | SWAP %.1f%% | TEMP %.1f°C | "
            "NVMe %.1f°C | LOAD/CPU %.2f | D %d | i915-D %d | ZABBIX %s",
            snapshot["cpu"]["util"],
            snapshot["memory"]["util"],
            snapshot["memory"]["swap_util"],
            snapshot["temperature"]["cpu_max"],
            snapshot["temperature"]["nvme_max"],
            snapshot["cpu"]["load_per_cpu"],
            snapshot["process"]["d_count"],
            snapshot["process"]["i915_d_count"],
            self._zabbix_state(),
        )

    def _handle_incidents(
        self,
        snapshot: dict[str, Any],
        process_rows: list[dict[str, Any]],
        now: float,
    ) -> None:
        """Capture forensic evidence for sustained diagnostic conditions."""
        sustained_reasons = self._sustained(evaluate(snapshot, self.cfg))
        if not sustained_reasons:
            return

        cooldown = float(self.cfg.get("limits", {}).get("incident_cooldown_seconds", 120))
        if now - self.last_incident <= cooldown:
            return

        reason = " | ".join(sustained_reasons)
        self.logger.critical("Condición sostenida: %s", reason)
        report = capture(
            self.cfg["app"]["incident_directory"],
            reason,
            snapshot,
            process_rows,
        )
        self.logger.warning("Incidente guardado: %s", report)
        self.last_incident = now

    def _handle_zabbix(self, snapshot: dict[str, Any]) -> None:
        """Send the current snapshot to Zabbix when the interval is due."""
        if not self.zabbix.due():
            return
        metrics = build_metrics(snapshot, self.cfg.get("watchlist", []))
        self.zabbix.send(metrics)

    def run(self) -> None:
        """Run the continuous read-only monitoring loop."""
        self.logger.info(
            "Iniciando PC Guardian Ubuntu v%s",
            __version__,
        )
        self.logger.info("Host: %s | Kernel: %s", platform.node(), platform.release())
        self.logger.info("Adquiriendo datos del sistema...")

        zabbix_cfg = self.cfg.get("zabbix", {})
        if zabbix_cfg.get("enabled", False):
            self.logger.info(
                "Zabbix habilitado: %s:%s | host=%s",
                zabbix_cfg.get("server", ""),
                zabbix_cfg.get("port", 10051),
                zabbix_cfg.get("host", ""),
            )
        else:
            self.logger.warning("Zabbix está deshabilitado en config/config.yaml")

        sample_interval = float(self.cfg.get("app", {}).get("sample_interval_seconds", 2))
        summary_interval = float(self.cfg.get("app", {}).get("console_summary_seconds", 10))

        while True:
            snapshot, process_rows = self.collect_snapshot()
            now = time.monotonic()

            if now - self.last_summary >= summary_interval:
                self._summary(snapshot)
                self.last_summary = now

            self._handle_incidents(snapshot, process_rows, now)
            self._handle_zabbix(snapshot)
            time.sleep(sample_interval)
