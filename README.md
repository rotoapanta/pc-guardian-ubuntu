# PC Guardian Ubuntu v2.4.9

Sistema **solo lectura** de diagnóstico y monitoreo para estaciones de trabajo Ubuntu. Su objetivo es conservar evidencia útil ante congelamientos y degradación del sistema y enviar telemetría a Zabbix 7.

## Alcance de seguridad

PC Guardian **no mata procesos, no reinicia servicios, no ejecuta remediaciones y no crea Zabbix Actions**. El runtime se limita a adquirir datos, evaluar condiciones, registrar evidencia y enviar métricas.

## Funciones principales

- CPU: utilización, load 1m/5m y load normalizado por CPU lógica.
- RAM y swap: utilización y memoria disponible.
- Disco: utilización de `/`, espacio libre y throughput agregado de lectura/escritura.
- Temperaturas: CPU Intel y NVMe mediante `psutil`/`lm-sensors`.
- PSI Linux: CPU, memoria e I/O (`some avg10`).
- Procesos: cantidad total, D-state, i915 D-state y watchlist configurable.
- Incidentes JSON: snapshot, top processes, stacks D-state y mensajes i915/DRM.
- Zabbix Sender: 32 métricas con la watchlist predeterminada.
- Provisionamiento Zabbix idempotente: 32 Items, 12 Triggers y 7 Graphs.

## Arquitectura

```text
pc-guardian-ubuntu/
├── main.py
├── core/
├── monitors/
├── diagnostics/
├── integrations/
├── web/                     # API FastAPI opcional
├── config/
├── logs/
├── data/incidents/
├── scripts/
├── systemd/
├── zabbix/
│   ├── provisioning/
│   └── templates/README.md
├── tests/
├── pyproject.toml
├── requirements.txt
├── README.md
├── README_EN.md
├── CHANGELOG.md
├── VERSION
└── LICENSE
```

## Instalación

```bash
cd pc-guardian-ubuntu
chmod +x scripts/*.sh
./scripts/install.sh
```

El instalador crea el entorno:

```text
pc-guardian-ubuntu-env
```

Actívalo en cada terminal nueva:

```bash
source pc-guardian-ubuntu-env/bin/activate
```

## Configuración

Edite:

```text
config/config.yaml
```

El nombre `zabbix.host` debe coincidir exactamente con el **Host name** creado manualmente en Zabbix.

Para el token API puede usar el YAML local o, preferiblemente:

```bash
export ZABBIX_API_TOKEN='TOKEN_REAL'
```

El archivo `config/config.yaml` está ignorado por Git.

## Zabbix Sender

En Ubuntu 24.04:

```bash
./scripts/install_zabbix_sender.sh
```

## Provisionamiento Zabbix

```bash
python zabbix/provisioning/provision.py
```

o:

```bash
./scripts/provision_zabbix.sh
```

El provisionador crea/verifica:

- Host Group: `Ubuntu Desktop`
- Template Group: `Templates/Ubuntu`
- Template: `Ubuntu Desktop`
- 32 Items con la watchlist predeterminada
- 12 Triggers
- 7 Graphs

**No crea hosts y no crea Actions.** Los hosts se crean manualmente y se vinculan al grupo/template desde la interfaz de Zabbix.

## Ejecución

```bash
python main.py
```

Estado inicial esperado:

```text
ZABBIX PENDING
```

Tras el primer envío correcto:

```text
SUCCESS | Métricas enviadas correctamente a Zabbix
ZABBIX OK
```

## Validación completa

```bash
./scripts/validate_project.sh
```

Ejecuta compilación, tests y `ruff`.

## Unidades Zabbix

- memoria y capacidad de disco: `B`
- throughput: `Bps`
- temperaturas: `°C`
- CPU/RAM/swap/PSI: `%`
- cargas y contadores: sin unidad

Zabbix realiza el escalado visual automático para bytes y bytes/s.

## Incidentes

Los eventos sostenidos se guardan en:

```text
data/incidents/
```

Incluyen evidencia de diagnóstico, pero PC Guardian no intenta corregir el sistema automáticamente.
