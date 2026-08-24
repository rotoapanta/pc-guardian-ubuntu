#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV="$ROOT/pc-guardian-ubuntu-env"
cd "$ROOT"

echo "[INFO] Instalando dependencias Ubuntu..."
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip lm-sensors

if [ ! -d "$ENV" ]; then
    echo "[INFO] Creando entorno virtual pc-guardian-ubuntu-env..."
    python3 -m venv "$ENV"
else
    echo "[INFO] Entorno virtual existente: $ENV"
fi

"$ENV/bin/python" -m pip install --upgrade pip setuptools wheel
"$ENV/bin/python" -m pip install -e ".[dev,web]"

if [ ! -f config/config.yaml ]; then
    cp config/config.example.yaml config/config.yaml
    echo "[INFO] Creado config/config.yaml desde el ejemplo."
fi

mkdir -p logs data/incidents
touch logs/.gitkeep data/.gitkeep data/incidents/.gitkeep

echo "[SUCCESS] Instalación terminada"
echo
echo "Activar entorno:"
echo "  source pc-guardian-ubuntu-env/bin/activate"
echo
echo "Ejecutar:"
echo "  python main.py"
