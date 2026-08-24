# PC Guardian Ubuntu v2.4.9

Read-only diagnostics and monitoring for Ubuntu desktop workstations, focused on preserving freeze evidence and exporting telemetry to Zabbix 7.

PC Guardian does **not** kill processes, restart services, perform remediation, or provision Zabbix Actions. It only collects, diagnoses, records, and reports.

## Install

```bash
chmod +x scripts/*.sh
./scripts/install.sh
source pc-guardian-ubuntu-env/bin/activate
```

## Run

```bash
python main.py
```

## Zabbix provisioning

```bash
export ZABBIX_API_TOKEN='REAL_TOKEN'
python zabbix/provisioning/provision.py
```

The provisioner manages the Host Group, Template Group, Template, 32 default Items, 12 Triggers, and 7 Graphs. Hosts are created manually in Zabbix.

## Validate

```bash
./scripts/validate_project.sh
```
