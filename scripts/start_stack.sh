#!/bin/bash
set -e

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
sleep 3
echo ""

bash /home/markmur88/Simulador/scripts/ports_stop.sh

SUPERVISOR_CONF="/home/markmur88/Simulador/config/supervisor_simulador.conf"

manage_supervised() {
    local svc="$1"
    local status
    status=$(supervisorctl -c "$SUPERVISOR_CONF" status "$svc" | awk '{print $2}')
    if [[ "$status" == "RUNNING" ]]; then
        echo "🔄 $svc ya está activo. Reiniciando..."
        supervisorctl -c "$SUPERVISOR_CONF" restart "$svc"
    else
        echo "▶️ $svc no está activo. Iniciando..."
        supervisorctl -c "$SUPERVISOR_CONF" start "$svc"
    fi
}


# cerrar procesos en puertos Tor (9053/9054)
for port in 9053 9054; do
    pid=$(lsof -ti tcp:$port 2>/dev/null || true)
    if [[ $pid ]]; then
        echo "⚠️  Cerrando proceso en puerto $port (PID $pid)"
        sudo kill -9 $pid
    fi
done
echo ""
sleep 3
echo ""

# matar cualquier Tor residual
sudo pgrep tor | while read -r pid; do
    echo "⚠️  Matando Tor PID $pid"
    sudo kill -9 "$pid"
done
echo ""
sleep 3
echo ""

# ─── 2) Preparar Django ─────────────────────────────────────────────────────────
echo "🛠️  Ejecutando migraciones y colectando estáticos…"
cd "$SIM_DIR"
source ~/envAPP/bin/activate
pip3 install -r ~/api_bank_h2/requirements.txt
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

# asegurar permisos del hidden service
chmod 700 "$BASE_DIR/tor_data/hidden_service"
chown -R markmur88: "$BASE_DIR/tor_data"
echo ""
sleep 3
echo ""
# ─── 3) Verificar torrc y arrancar Tor ──────────────────────────────────────────
echo "🔍 Verificando torrc…"
tor -f "$TORRC" --verify-config \
    || { echo "❌ torrc inválido, chequealo antes de continuar"; exit 1; }

echo "🧅 Iniciando Tor…"
tor -f "$TORRC" &
TOR_PID=$!
echo ""
sleep 3
echo ""
# esperar generación del .onion
echo -n "⌛ Esperando a que Tor genere el .onion… "
for i in {1..10}; do
    if [ -f "$TOR_DIR/hostname" ]; then
        echo "✅"
        break
    fi
    sleep 1
done
echo ""
sleep 3
echo ""
if [ ! -f "$TOR_DIR/hostname" ]; then
    echo "❌ No se generó el .onion en tiempo esperado."
    exit 1
fi
echo ""
sleep 3
echo ""
ONION_ADDR=$(cat "$TOR_DIR/hostname")
echo "🧅 Servicio oculto disponible en: $ONION_ADDR"
echo ""
sleep 3
echo ""
# ─── 4) Inyectar ALLOWED_HOSTS y arrancar supervisord ───────────────────────────
export DJANGO_ALLOWED_HOSTS="127.0.0.1,$PUBLIC_IP,$ONION_ADDR"
echo "🛡️  DJANGO_ALLOWED_HOSTS set to: $DJANGO_ALLOWED_HOSTS"
echo ""
sleep 3
echo ""


echo "🔄 Iniciando supervisord…"
supervisord -c "$SUPERVISORD_CONF"
sleep 3

echo "▶️ Servicios arrancados:"
supervisorctl -c "$SUPERVISORD_CONF" status

sleep 3
echo ""
