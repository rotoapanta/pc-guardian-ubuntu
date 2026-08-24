#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV="$ROOT/pc-guardian-ubuntu-env"

if [ ! -x "$ENV/bin/python" ]; then
    echo "[ERROR] Ejecute primero ./scripts/install.sh"
    exit 1
fi

cd "$ROOT"
exec "$ENV/bin/python" zabbix/provisioning/provision.py
