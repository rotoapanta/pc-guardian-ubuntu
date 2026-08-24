#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV="$ROOT/pc-guardian-ubuntu-env"

if [ ! -x "$ENV/bin/python" ]; then
    echo "[ERROR] Ejecute primero ./scripts/install.sh"
    exit 1
fi

cd "$ROOT"

echo "[INFO] Compilando módulos Python..."
"$ENV/bin/python" -m compileall -q main.py core monitors diagnostics integrations web zabbix tests

echo "[INFO] Ejecutando pytest..."
"$ENV/bin/python" -m pytest -q

echo "[INFO] Ejecutando ruff..."
"$ENV/bin/python" -m ruff check main.py core monitors diagnostics integrations web zabbix tests

echo "[SUCCESS] Validación completada"
