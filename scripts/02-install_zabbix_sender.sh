#!/usr/bin/env bash

set -euo pipefail

# ============================================================
# PC Guardian Ubuntu
# Instalador de Zabbix Sender
# Ubuntu 24.04 / Zabbix 7.0
# ============================================================

ZABBIX_VERSION="7.0"
UBUNTU_VERSION="24.04"

echo "============================================================"
echo " PC GUARDIAN UBUNTU - Instalación de Zabbix Sender"
echo "============================================================"

# ------------------------------------------------------------
# 1. Verificar sistema operativo
# ------------------------------------------------------------

if [ ! -f /etc/os-release ]; then
    echo "[ERROR] No se pudo identificar el sistema operativo."
    exit 1
fi

source /etc/os-release

echo "[INFO] Sistema detectado: ${PRETTY_NAME}"

if [ "${ID}" != "ubuntu" ]; then
    echo "[ERROR] Este instalador está diseñado para Ubuntu."
    exit 1
fi

if [ "${VERSION_ID}" != "${UBUNTU_VERSION}" ]; then
    echo "[WARNING] Versión detectada: ${VERSION_ID}"
    echo "[WARNING] Este proyecto fue validado para Ubuntu ${UBUNTU_VERSION}."
fi

# ------------------------------------------------------------
# 2. Verificar si ya está instalado
# ------------------------------------------------------------

if command -v zabbix_sender >/dev/null 2>&1; then
    echo "[OK] zabbix_sender ya está instalado."
    echo
    zabbix_sender --version | head -1
    echo
    echo "[SUCCESS] No es necesario realizar ninguna instalación."
    exit 0
fi

# ------------------------------------------------------------
# 3. Instalar dependencias
# ------------------------------------------------------------

echo "[INFO] Instalando dependencias..."

sudo apt-get update
sudo apt-get install -y wget ca-certificates

# ------------------------------------------------------------
# 4. Instalar repositorio oficial Zabbix
# ------------------------------------------------------------

echo "[INFO] Configurando repositorio oficial Zabbix ${ZABBIX_VERSION}..."

ZABBIX_RELEASE_URL="https://repo.zabbix.com/zabbix/${ZABBIX_VERSION}/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest+ubuntu24.04_all.deb"

TMP_FILE="/tmp/zabbix-release_latest+ubuntu24.04_all.deb"

wget -O "${TMP_FILE}" "${ZABBIX_RELEASE_URL}"

sudo dpkg -i "${TMP_FILE}"

rm -f "${TMP_FILE}"

# ------------------------------------------------------------
# 5. Actualizar repositorios
# ------------------------------------------------------------

echo "[INFO] Actualizando repositorios..."

sudo apt-get update

# ------------------------------------------------------------
# 6. Instalar Zabbix Sender
# ------------------------------------------------------------

echo "[INFO] Instalando zabbix-sender..."

sudo apt-get install -y zabbix-sender

# ------------------------------------------------------------
# 7. Verificación
# ------------------------------------------------------------

if ! command -v zabbix_sender >/dev/null 2>&1; then
    echo "[ERROR] zabbix_sender no quedó instalado correctamente."
    exit 1
fi

ZABBIX_SENDER_PATH="$(command -v zabbix_sender)"

echo
echo "============================================================"
echo "[SUCCESS] Zabbix Sender instalado correctamente"
echo "============================================================"
echo
echo "Ejecutable:"
echo "  ${ZABBIX_SENDER_PATH}"
echo
echo "Versión:"
zabbix_sender --version | head -1
echo
echo "PC Guardian podrá utilizar:"
echo "  ${ZABBIX_SENDER_PATH}"
echo