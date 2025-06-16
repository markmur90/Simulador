#!/bin/bash
set +e

# ─── Configuración ─────────────────────────────────────────────────────────────
BASE_DIR="/home/markmur88/Simulador"
SIM_DIR="$BASE_DIR/simulador_banco"
TOR_DIR="$BASE_DIR/tor_data/hidden_service"
SUPERVISORD_CONF="$BASE_DIR/config/supervisor_simulador.conf"
TORRC="$BASE_DIR/config/torrc_simulador"
PUBLIC_IP="80.78.30.242"  # tu IP pública

# ─── 1) Limpieza de procesos previos ────────────────────────────────────────────
echo "🧹 Limpiando procesos previos…"
pkill -f "supervisord.*$SUPERVISORD_CONF"      2>/dev/null || true
pkill -f "gunicorn.*simulador_banco.wsgi"     2>/dev/null || true
pkill -f "tor.*$TORRC"                         2>/dev/null || true
echo ""
sleep 2
echo ""

bash /home/markmur88/Simulador/scripts/ports_stop.sh

SUPERVISOR_CONF="/home/markmur88/Simulador/config/supervisor_simulador.conf"

manage_supervised() {
    local svc="$1"
    local status
    status=$(sudo supervisorctl -c "$SUPERVISOR_CONF" status "$svc" | awk '{print $2}')
    if [[ "$status" == "RUNNING" ]]; then
        echo "🔄 $svc ya está activo. Reiniciando..."
        sudo supervisorctl -c "$SUPERVISOR_CONF" restart "$svc"
    else
        echo "▶️ $svc no está activo. Iniciando..."
        sudo supervisorctl -c "$SUPERVISOR_CONF" start "$svc"
    fi
}

sudo chown -R markmur88:markmur88 /home/markmur88/Simulador/tor_data/hidden_service

# matar cualquier Tor residual
sudo pgrep tor | while read -r pid; do
    echo "⚠️  Matando Tor PID $pid"
    sudo kill -9 "$pid"
done
echo ""
sleep 2
echo ""

# ─── 2) Preparar Django ─────────────────────────────────────────────────────────
echo "🛠️  Ejecutando migraciones y colectando estáticos…"
cd "$SIM_DIR"
source /home/markmur88/envSIM/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
echo ""
sleep 2
echo ""

python3 manage.py migrate
echo ""
sleep 2
echo ""
python3 manage.py collectstatic --noinput
echo ""
sleep 2
echo ""

# asegurar permisos del hidden service
# sudo chown -R markmur88:markmur88 /home/markmur88/Simulador/tor_data
# sudo chmod -R 700        /home/markmur88/Simulador/tor_data
# sudo mkdir -p /home/markmur88/Simulador/logs
# sudo chown markmur88:markmur88 /home/markmur88/Simulador/logs
# sudo chmod 755             /home/markmur88/Simulador/logs

# echo ""
# sleep 2
# echo ""


# ─── 3) Verificar torrc y arrancar Tor ──────────────────────────────────────────
echo "🔍 Verificando torrc…"
tor -f "$TORRC" --verify-config \
    || { echo "❌ torrc inválido, chequealo antes de continuar"; exit 1; }

echo ""
sleep 10
echo ""

# echo "🧅 Iniciando Tor…"
# tor -f "$TORRC" &
# TOR_PID=$!
# echo ""
# sleep 3
# echo ""

# sudo -u markmur88 -H bash -c "cd /home/markmur88/Simulador && /usr/bin/tor -f config/torrc_simulador &"

sleep 3

# esperar generación del .onion
echo -n "⌛ Esperando a que Tor genere el .onion… "
for i in {1..20}; do
    if [ -f "$TOR_DIR/hostname" ]; then
        echo "✅"
        break
    fi
    sleep 5
done
echo ""
sleep 5
echo ""

# if [ ! -f "$TOR_DIR/hostname" ]; then
#     echo "❌ No se generó el .onion en tiempo esperado."
#     exit 0
# fi
# echo ""
# sleep 5
# echo ""
ONION_ADDR=$(cat "$TOR_DIR/hostname")
echo "🧅 Servicio oculto disponible en: $ONION_ADDR"
echo ""
sleep 5
echo ""
# ─── 4) Inyectar ALLOWED_HOSTS y arrancar supervisord ───────────────────────────
export DJANGO_ALLOWED_HOSTS="127.0.0.1,0.0.0.0,$PUBLIC_IP,$ONION_ADDR"
echo "🛡️  DJANGO_ALLOWED_HOSTS set to: $DJANGO_ALLOWED_HOSTS"
echo ""
sleep 5
echo ""

# ─── Asegurar existencia de logs y socket ─────────────────────────────────────
LOG_DIR="$BASE_DIR/logs"
SOCK="$LOG_DIR/supervisord.sock"

echo "🗂️  Creando directorio de logs si no existe…"
mkdir -p "$LOG_DIR"
chown -R markmur88 "$LOG_DIR"
chmod 755 "$LOG_DIR"
echo ""
sleep 5

# ─── Iniciar supervisord y esperar socket ────────────────────────────────────
echo "🔄 Iniciando supervisord…"
supervisord -c "$SUPERVISOR_CONF"
sleep 5

# Esperar a que supervisord cree el socket
echo -n "⌛ Esperando a que aparezca supervisord.sock… "
for i in {1..20}; do
  if [ -S "$SOCK" ]; then
    echo "✅"
    break
  fi
  sleep 1
done
echo ""
sleep 15


# supervisorctl -c "$SUPERVISOR_CONF" reread
# supervisorctl -c "$SUPERVISOR_CONF" update
# supervisorctl -c "$SUPERVISOR_CONF" restart tor

# echo "🔄 Iniciando supervisord…"
# supervisord -c "$SUPERVISORD_CONF"
# sleep 3
# echo ""

echo "▶️ Servicios arrancados:"
supervisorctl -c "$SUPERVISORD_CONF" status
sleep 3
echo ""
