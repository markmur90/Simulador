#!/bin/bash
set -e

bash /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/scripts/ports_stop.sh


SUPERVISOR_CONF="/home/markmur88/api_bank_h2/scripts/utils/simulator_bank/config/supervisor_simulador.conf"

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

cd /home/markmur88/api_bank_h2/scripts/utils/simulator_bank

echo "📦 Creando entorno virtual y preparando entorno de trabajo..."
python -m venv venv
source venv/bin/activate

echo "⬆️  Actualizando pip e instalando dependencias..."
pip install --upgrade pip
pip install -r /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/simulador_banco/requirements.txt

echo "✅ Dependencias instaladas correctamente"
echo "▶️ Iniciando servicio de supervisión (supervisord)..."

supervisord -c /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/config/supervisor_simulador.conf

supervisorctl -c "$SUPERVISOR_CONF" status
