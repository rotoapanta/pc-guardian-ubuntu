#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
USER_NAME="${SUDO_USER:-$USER}"
ENV="$ROOT/pc-guardian-ubuntu-env"

if [ ! -x "$ENV/bin/python" ]; then
    echo "[ERROR] Ejecute primero ./scripts/install.sh"
    exit 1
fi

sudo tee /etc/systemd/system/pc-guardian.service >/dev/null <<EOF
[Unit]
Description=PC Guardian Ubuntu
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$USER_NAME
WorkingDirectory=$ROOT
ExecStart=$ENV/bin/python $ROOT/main.py
Restart=on-failure
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now pc-guardian
sudo systemctl status pc-guardian --no-pager
