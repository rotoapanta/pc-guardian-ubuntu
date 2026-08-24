<p align="right"><a href="README.md">English</a></p>

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

**PC Guardian Ubuntu** es un agente de diagnóstico y monitoreo de solo lectura para estaciones de trabajo Ubuntu.

Recopila telemetría del sistema operativo, detecta condiciones sostenidas, conserva evidencia de congelamientos, monitorea procesos en estado D y eventos relacionados con Intel `i915`, y exporta métricas a **Zabbix 7**.

PC Guardian está diseñado como un **sistema de diagnóstico y monitoreo únicamente**. No termina procesos, no reinicia servicios, no cambia prioridades ni ejecuta acciones automáticas de remediación.

---

## ✨ Características

- Arquitectura de solo lectura.
- Monitoreo de CPU, RAM, swap, disco y temperaturas.
- Monitoreo Linux PSI.
- Monitoreo de procesos.
- Detección D-state.
- Diagnóstico Intel i915.
- Evidencia de congelamientos.
- Integración con Zabbix Sender.
- Aprovisionamiento Zabbix automático e idempotente.
- 32 items Zabbix.
- 12 triggers.
- 7 gráficas.
- Logging profesional.
- Integración con systemd.
- Validación con pytest y Ruff.
- Docstrings y type hints.

---

## 🛠️ Requisitos

| Componente | Requisito |
|-----------|-----------|
| Sistema operativo | Ubuntu 24.04 LTS |
| Python | 3.12+ |
| Zabbix Server | 7.0.x |
| Zabbix Sender | 7.0.x recomendado |
| systemd | Requerido para modo servicio |
| lm-sensors | Requerido para temperaturas |
| Linux PSI | `/proc/pressure` habilitado |
| Intel i915 | Opcional |

---

## 🗂️ Estructura del proyecto

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

## 🚀 Instalación

```bash
cd ~/Documentos/Projects
git clone git@github.com:rotoapanta/pc-guardian-ubuntu.git
cd pc-guardian-ubuntu

chmod +x scripts/*.sh
./scripts/01-install.sh
source pc-guardian-ubuntu-env/bin/activate
```

---

## ⚙️ Configuración

```bash
cp config/config.example.yaml config/config.yaml
nano config/config.yaml
```

Nunca publiques `config/config.yaml` con credenciales o tokens API.

---

## 📡 Zabbix Sender

```bash
./scripts/02-install_zabbix_sender.sh
```

---

## ✅ Validación

```bash
./scripts/03-validate_project.sh
```

Resultado esperado:

```text
10 passed
All checks passed!
[SUCCESS] Validación completada
```

---

## 📊 Aprovisionamiento Zabbix

```bash
./scripts/04-provision_zabbix.sh
```

| Objeto | Definición |
|--------|------------|
| Host Group | `Ubuntu Desktop` |
| Template Group | `Templates/Ubuntu` |
| Template | `Ubuntu Desktop` |
| Items | 32 |
| Triggers | 12 |
| Graphs | 7 |

Los hosts se crean manualmente en Zabbix.

---

## 📈 Principales métricas

| Métrica | Key | Unidad |
|--------|-----|--------|
| Utilización CPU | `pcguardian.cpu.util` | `%` |
| Temperatura CPU | `pcguardian.cpu.temperature` | `°C` |
| Temperatura NVMe | `pcguardian.nvme.temperature` | `°C` |
| Utilización memoria | `pcguardian.memory.util` | `%` |
| Memoria disponible | `pcguardian.memory.available` | `B` |
| Utilización swap | `pcguardian.swap.util` | `%` |
| Uso disco raíz | `pcguardian.disk.root.util` | `%` |
| Disco raíz libre | `pcguardian.disk.root.free` | `B` |
| Lectura disco | `pcguardian.disk.read` | `Bps` |
| Escritura disco | `pcguardian.disk.write` | `Bps` |
| PSI CPU avg10 | `pcguardian.psi.cpu.avg10` | `%` |
| PSI memoria avg10 | `pcguardian.psi.memory.avg10` | `%` |
| PSI I/O avg10 | `pcguardian.psi.io.avg10` | `%` |
| Conteo procesos | `pcguardian.process.count` | — |
| Conteo D-state | `pcguardian.process.dstate.count` | — |
| Conteo i915 D-state | `pcguardian.process.i915.dstate.count` | — |

---

## 🚨 Triggers Zabbix

Los 12 triggers cubren CPU, temperaturas, disco, presión de memoria, swap combinado con presión de memoria, I/O, D-state e Intel i915.

---

## 📉 Gráficas Zabbix

1. Ubuntu Desktop: CPU
2. Ubuntu Desktop: Temperatures
3. Ubuntu Desktop: Memory and Swap
4. Ubuntu Desktop: Disk Utilization
5. Ubuntu Desktop: Disk I/O
6. Ubuntu Desktop: PSI Pressure
7. Ubuntu Desktop: D-State and i915

---

## 🔍 Diagnóstico del sistema

```bash
./scripts/05-system_diagnostic.sh
```

---

## ▶️ Ejecución manual

```bash
source pc-guardian-ubuntu-env/bin/activate
python3 main.py
```

---

## ⚙️ Servicio systemd

Instalar:

```bash
./scripts/06-install_systemd.sh
```

Estado:

```bash
systemctl status pc-guardian.service --no-pager -l
```

Logs:

```bash
journalctl -u pc-guardian.service -f
```

Desinstalar:

```bash
./scripts/07-uninstall_systemd.sh
```

---

## 🔒 Diseño de solo lectura

PC Guardian puede recopilar, diagnosticar, preservar evidencia y exportar telemetría a Zabbix.

PC Guardian **no** mata procesos, no envía SIGTERM/SIGKILL, no reinicia procesos o servicios, no cambia prioridades, no ejecuta remediaciones y no modifica parámetros del kernel.

---

## 🔐 Seguridad

Se excluyen de Git:

```text
config/config.yaml
.env
.env.*
pc-guardian-ubuntu-env/
logs/
data/incidents/
```

---

## 🧪 Desarrollo

```bash
source pc-guardian-ubuntu-env/bin/activate
python3 -m pytest -v
./scripts/03-validate_project.sh
```

---

## 💬 Feedback

robertocarlos.toapanta@gmail.com

## 🛟 Soporte

robertocarlos.toapanta@gmail.com

## 📄 Licencia

Consulte [LICENSE](LICENSE).

## 👥 Autores

- [@rotoapanta](https://github.com/rotoapanta)

---

## 📜 Changelog

### [Unreleased]

-

### 2.4.9 – 2026-08-24

- Consolidación como sistema de diagnóstico y monitoreo de solo lectura.
- Eliminación de remediación automática.
- Manejo centralizado de versión.
- Aprovisionamiento Zabbix.
- 32 items, 12 triggers y 7 gráficas.
- Monitoreo PSI, D-state e Intel i915.
- Evidencia de incidentes.
- Integración systemd.
- Validación, tests y Ruff.

---

## 🔗 Enlaces

[![GitHub](https://img.shields.io/badge/GitHub-rotoapanta-181717?style=for-the-badge&logo=github)](https://github.com/rotoapanta)

[![LinkedIn](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/roberto-carlos-toapanta-g/)

[![Twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/rotoapanta)
