#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ENV="$ROOT/pc-guardian-ubuntu-env"

if [ ! -x "$ENV/bin/python" ]; then
    echo "[ERROR] Ejecute primero ./scripts/01-install.sh"
    exit 1
fi

PYTHON="$ENV/bin/python"
PYTEST="$ENV/bin/pytest"
RUFF="$ENV/bin/ruff"

cd "$ROOT"

echo "[INFO] Compilando módulos Python..."

"$PYTHON" -m compileall \
    main.py \
    core \
    monitors \
    diagnostics \
    integrations \
    zabbix \
    tests

echo "[INFO] Ejecutando pytest..."

"$PYTEST" -q

echo "[INFO] Ejecutando ruff..."

"$RUFF" check \
    main.py \
    core \
    monitors \
    diagnostics \
    integrations \
    zabbix \
    tests

echo "[SUCCESS] Validación completada"