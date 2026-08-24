<p align="right"><a href="README.es.md">Español</a></p>

# <p align="center">PC Guardian Ubuntu</p>

<p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://ubuntu.com/"><img src="https://img.shields.io/badge/Ubuntu-24.04%20LTS-E95420?logo=ubuntu&logoColor=white" alt="Ubuntu"></a>
    <a href="https://www.zabbix.com/"><img src="https://img.shields.io/badge/Zabbix-7.0.x-D40000" alt="Zabbix"></a>
    <a href="https://github.com/rotoapanta/pc-guardian-ubuntu/issues"><img src="https://img.shields.io/github/issues/rotoapanta/pc-guardian-ubuntu" alt="GitHub issues"></a>
    <a href="https://github.com/rotoapanta/pc-guardian-ubuntu"><img src="https://img.shields.io/github/repo-size/rotoapanta/pc-guardian-ubuntu" alt="GitHub repo size"></a>
    <a href="https://github.com/rotoapanta/pc-guardian-ubuntu/commits"><img src="https://img.shields.io/github/last-commit/rotoapanta/pc-guardian-ubuntu" alt="GitHub last commit"></a>
    <a href="https://www.linux.org/"><img src="https://img.shields.io/badge/Platform-Linux-orange" alt="Linux"></a>
    <a href="https://github.com/rotoapanta/pc-guardian-ubuntu/blob/main/LICENSE"><img src="https://img.shields.io/github/license/rotoapanta/pc-guardian-ubuntu" alt="License"></a>
    <a href="https://www.linkedin.com/in/roberto-carlos-toapanta-g/"><img src="https://img.shields.io/badge/Author-Roberto%20Toapanta-brightgreen" alt="Author"></a>
    <a href="#-changelog"><img src="https://img.shields.io/badge/Version-2.4.9-brightgreen" alt="Version"></a>
    <a href="https://github.com/rotoapanta/pc-guardian-ubuntu/fork"><img src="https://img.shields.io/github/forks/rotoapanta/pc-guardian-ubuntu?style=social" alt="GitHub forks"></a>
</p>

**PC Guardian Ubuntu** is a read-only diagnostic and monitoring agent for Ubuntu workstations.

It continuously collects operating-system telemetry, detects sustained diagnostic conditions, preserves freeze evidence, monitors D-state and Intel `i915` related processes, and exports metrics to **Zabbix 7** for centralized visualization, historical analysis, graphs, and trigger evaluation.

PC Guardian is intentionally designed as a **diagnostic and monitoring system only**. It does not terminate processes, restart services, renice applications, or execute automatic remediation actions.

---

## ✨ Features

- Read-only architecture.
- CPU, RAM, swap, disk and temperature monitoring.
- Linux PSI monitoring.
- Process, D-state and Intel i915 diagnostics.
- Freeze evidence collection.
- Zabbix Sender integration.
- Automatic, idempotent Zabbix provisioning.
- 32 Zabbix items.
- 12 Zabbix triggers.
- 7 predefined graphs.
- Professional logging.
- systemd integration.
- Automated validation with pytest and Ruff.
- Docstrings and type hints.

---

## 🛠️ System Requirements

| Component | Requirement |
|-----------|-------------|
| Operating System | Ubuntu 24.04 LTS |
| Python | 3.12+ |
| Zabbix Server | 7.0.x |
| Zabbix Sender | 7.0.x recommended |
| systemd | Required for service mode |
| lm-sensors | Required for temperature monitoring |
| Linux PSI | `/proc/pressure` enabled |
| Intel i915 | Optional |

---

## 🗂️ Project Structure

```text
pc-guardian-ubuntu/
├── main.py
├── core/
├── monitors/
├── diagnostics/
├── integrations/
├── config/
├── data/
├── logs/
├── scripts/
│   ├── 01-install.sh
│   ├── 02-install_zabbix_sender.sh
│   ├── 03-validate_project.sh
│   ├── 04-provision_zabbix.sh
│   ├── 05-system_diagnostic.sh
│   ├── 06-install_systemd.sh
│   └── 07-uninstall_systemd.sh
├── systemd/
├── tests/
├── zabbix/
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── README.es.md
├── requirements.txt
├── pyproject.toml
└── VERSION
```

---

## 🚀 Installation

```bash
cd ~/Documentos/Projects
git clone git@github.com:rotoapanta/pc-guardian-ubuntu.git
cd pc-guardian-ubuntu

chmod +x scripts/*.sh
./scripts/01-install.sh
source pc-guardian-ubuntu-env/bin/activate
```

---

## ⚙️ Configuration

```bash
cp config/config.example.yaml config/config.yaml
nano config/config.yaml
```

Never commit `config/config.yaml` with credentials or API tokens.

---

## 📡 Zabbix Sender

```bash
./scripts/02-install_zabbix_sender.sh
```

---

## ✅ Project Validation

```bash
./scripts/03-validate_project.sh
```

Expected:

```text
10 passed
All checks passed!
[SUCCESS] Validación completada
```

---

## 📊 Zabbix Provisioning

```bash
./scripts/04-provision_zabbix.sh
```

| Object | Definition |
|--------|------------|
| Host Group | `Ubuntu Desktop` |
| Template Group | `Templates/Ubuntu` |
| Template | `Ubuntu Desktop` |
| Items | 32 |
| Triggers | 12 |
| Graphs | 7 |

Hosts are created manually in Zabbix.

---

## 📈 Main Zabbix Metrics

| Metric | Key | Unit |
|--------|-----|------|
| CPU utilization | `pcguardian.cpu.util` | `%` |
| CPU temperature | `pcguardian.cpu.temperature` | `°C` |
| NVMe temperature | `pcguardian.nvme.temperature` | `°C` |
| Memory utilization | `pcguardian.memory.util` | `%` |
| Available memory | `pcguardian.memory.available` | `B` |
| Swap utilization | `pcguardian.swap.util` | `%` |
| Root disk utilization | `pcguardian.disk.root.util` | `%` |
| Root disk free | `pcguardian.disk.root.free` | `B` |
| Disk read | `pcguardian.disk.read` | `Bps` |
| Disk write | `pcguardian.disk.write` | `Bps` |
| PSI CPU avg10 | `pcguardian.psi.cpu.avg10` | `%` |
| PSI memory avg10 | `pcguardian.psi.memory.avg10` | `%` |
| PSI I/O avg10 | `pcguardian.psi.io.avg10` | `%` |
| Process count | `pcguardian.process.count` | — |
| D-state count | `pcguardian.process.dstate.count` | — |
| i915 D-state count | `pcguardian.process.i915.dstate.count` | — |

---

## 🚨 Zabbix Triggers

The template defines 12 diagnostic triggers covering:

- Missing data
- Sustained CPU load
- CPU temperature
- NVMe temperature
- Root filesystem utilization
- Memory pressure
- Swap combined with memory pressure
- I/O pressure
- Persistent D-state processes
- Persistent Intel i915 D-state processes

---

## 📉 Zabbix Graphs

1. Ubuntu Desktop: CPU
2. Ubuntu Desktop: Temperatures
3. Ubuntu Desktop: Memory and Swap
4. Ubuntu Desktop: Disk Utilization
5. Ubuntu Desktop: Disk I/O
6. Ubuntu Desktop: PSI Pressure
7. Ubuntu Desktop: D-State and i915

---

## 🔍 System Diagnostics

```bash
./scripts/05-system_diagnostic.sh
```

---

## ▶️ Manual Execution

```bash
source pc-guardian-ubuntu-env/bin/activate
python3 main.py
```

---

## ⚙️ systemd Service

Install:

```bash
./scripts/06-install_systemd.sh
```

Status:

```bash
systemctl status pc-guardian.service --no-pager -l
```

Logs:

```bash
journalctl -u pc-guardian.service -f
```

Uninstall:

```bash
./scripts/07-uninstall_systemd.sh
```

---

## 🔒 Read-Only Design

PC Guardian can:

```text
Collect
   ↓
Diagnose
   ↓
Preserve evidence
   ↓
Export telemetry
   ↓
Zabbix
```

PC Guardian does **not** kill processes, send SIGTERM/SIGKILL, restart processes or services, renice applications, execute remediation commands, or modify kernel parameters.

---

## 🔐 Security

Excluded from Git:

```text
config/config.yaml
.env
.env.*
pc-guardian-ubuntu-env/
logs/
data/incidents/
```

---

## 🧪 Development

```bash
source pc-guardian-ubuntu-env/bin/activate
python3 -m pytest -v
./scripts/03-validate_project.sh
```

---

## 💬 Feedback

robertocarlos.toapanta@gmail.com

## 🛟 Support

robertocarlos.toapanta@gmail.com

## 📄 License

See [LICENSE](LICENSE).

## 👥 Authors

- [@rotoapanta](https://github.com/rotoapanta)

---

## 📜 Changelog

This project follows Keep a Changelog and Semantic Versioning.

### [Unreleased]

-

### 2.4.9 – 2026-08-24

- Consolidated PC Guardian as a read-only diagnostic and monitoring system.
- Removed automatic remediation capabilities.
- Added centralized version handling.
- Added Zabbix Host Group, Template Group and Template provisioning.
- Added 32 items, 12 triggers and 7 graphs.
- Added Linux PSI, D-state and Intel i915 monitoring.
- Added incident evidence collection.
- Added idempotent Zabbix API provisioning.
- Added systemd integration.
- Added automated validation, tests and Ruff checks.

---

## 🔗 Links

[![GitHub](https://img.shields.io/badge/GitHub-rotoapanta-181717?style=for-the-badge&logo=github)](https://github.com/rotoapanta)

[![LinkedIn](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/roberto-carlos-toapanta-g/)

[![Twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/rotoapanta)
