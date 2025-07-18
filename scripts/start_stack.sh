#!/bin/bash
set -euo pipefail

# ─── Configuración ─────────────────────────────────────────────
BASE_DIR="/home/markmur88/Simulador"
SIM_DIR="$BASE_DIR/simulador_banco"
TOR_DATA="$BASE_DIR/tor_data/hidden_service"
SUPERVISORD_CONF="$BASE_DIR/config/supervisor_simulador.conf"
TORRC="$BASE_DIR/config/torrc_simulador"
PUBLIC_IP="80.78.30.242"

LOG_DIR="$BASE_DIR/logs"
REQS_PATH="$HOME/api_bank_h2/requirements.txt"
VENV_ACT="$HOME/envSIM/bin/activate"




# ─── 0) Pre-check de torrc ──────────────────────────────────────
echo "🔍 Verificando torrc…"
sudo tor --verify-config -f "$TORRC" \
  || { echo "❌ Error en torrc, corrígelo antes de continuar"; exit 1; }

echo ""
sleep 3
echo ""

# ─── 1) Detener Tor del sistema ────────────────────────────────
echo "🛑 Deteniendo Tor del sistema…"
sudo systemctl is-active --quiet tor && sudo systemctl stop tor
sudo systemctl disable tor || true

echo ""
sleep 3
echo ""

# ─── 2) Limpiar procesos previos ───────────────────────────────
echo "🧹 Limpiando procesos anteriores…"
pkill -f "supervisord.*$SUPERVISORD_CONF" 2>/dev/null || true
pkill -f "gunicorn.*simulador_banco.wsgi" 2>/dev/null || true
# matar cualquier tor residuo del usuario
pgrep -u "$(whoami)" tor | xargs --no-run-if-empty kill -9 || true

echo ""
sleep 3
echo ""

# ─── 3) Setup Django ──────────────────────────────────────────
echo "🛠  Migraciones y estáticos…"
cd "$SIM_DIR"
source "$VENV_ACT"
pip install -r "$REQS_PATH"
echo ""
sleep 3
echo ""
python manage.py makemigrations
echo ""
sleep 3
echo ""
python manage.py migrate
echo ""
sleep 3
echo ""
python manage.py collectstatic --noinput
echo ""
sleep 3
echo ""

# ─── 4) Ajustar permisos Tor data & logs ──────────────────────
echo "🔐 Permisos de tor_data y logs…"
# mkdir -p "$LOG_DIR" "$TOR_DATA"
# chown -R "$(whoami)" "$BASE_DIR/tor_data" "$LOG_DIR"
# chmod -R 700 "$BASE_DIR/tor_data"
# chmod -R 755 "$LOG_DIR"

sudo chown -R markmur88 /home/markmur88/Simulador/tor_data/hidden_service
sudo chmod 700                 /home/markmur88/Simulador/tor_data/hidden_service
sudo systemctl restart tor

echo ""
sleep 3
echo ""

# ─── 5) Supervisord: reread/update & arrancar servicios ───────
echo "♻️  Recargando supervisord…"
sudo supervisorctl -c "$SUPERVISORD_CONF" reread
sudo supervisorctl -c "$SUPERVISORD_CONF" update

echo ""
sleep 3
echo ""

echo "▶️ Iniciando servicios con supervisord…"
sudo supervisorctl -c "$SUPERVISORD_CONF" start all \
  || { echo "❌ No se pudieron iniciar todos los servicios"; exit 1; }

echo ""
sleep 3
echo ""

# ─── 6) Esperar a .onion y setear ALLOWED_HOSTS ─────────────
echo -n "⌛ Generando .onion… "
for i in {1..10}; do
  if [[ -f "$TOR_DATA/hostname" ]]; then
    echo "✅"
    break
  fi
  sleep 1
done
ONION_ADDR=$(< "$TOR_DATA/hostname")
echo "🧅 .onion: $ONION_ADDR"

echo ""
sleep 3
echo ""

export DJANGO_ALLOWED_HOSTS="127.0.0.1,$PUBLIC_IP,$ONION_ADDR"
echo "🛡  DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS"

echo ""
sleep 3
echo ""

# ─── 7) Estado final ──────────────────────────────────────────
echo ""
sudo supervisorctl -c "$SUPERVISORD_CONF" status

echo ""
sleep 3
echo ""
