#!/usr/bin/env bash
set -euo pipefail

sudo systemctl disable --now pc-guardian 2>/dev/null || true
sudo rm -f /etc/systemd/system/pc-guardian.service
sudo systemctl daemon-reload

echo "[OK] Servicio pc-guardian eliminado."
