# Changelog

## 2.4.9 - 2026-08-24

### Consolidation and Cleanup

- PC Guardian is now formally limited to read-only diagnostics and monitoring.
- Removed remaining Actions/remediation components and any related packaging references.
- Removed the obsolete YAML template; API provisioning is now the authoritative source.
- Updated `VERSION`, banner, configuration, FastAPI, and package metadata to version 2.4.9.
- Removed the virtual environment, logs, incidents, `__pycache__`, and `*.egg-info` from the package.
- Replaced the API token with `CHANGE_ME` and added support for the `ZABBIX_API_TOKEN` environment variable.
- Consolidated logging with standard levels plus `SUCCESS`; removed the `ACTION` level.
- Configuration, log, and incident paths are now resolved from the project root.
- Refined exception handling for PSI, temperature, incident, and i915 diagnostics.
- Preserved base units for memory/disk (`B`) and throughput (`Bps`).
- Preserved the Zabbix state transition `PENDING → OK/ERROR`.
- Harmonized local swap/PSI thresholds to reduce false positives.
- Zabbix provisioning remains idempotent for Items, Triggers, and Graphs.
- Updated tests to use the current keys and added coverage for item counts, units, and read-only behavior.
- Added `scripts/validate_project.sh` for `compileall` + `pytest` + `ruff`.

## 2.3.0 - 2026-08-20

- Initial modular architecture.
- Added Zabbix Sender integration and API provisioning.
- Added D-state/i915 diagnostics, PSI monitoring, temperature monitoring, and incident evidence collection.