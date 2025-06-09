#!/bin/bash
set -e

echo "🔁 Parando todas las instancias de supervisord..."

# Matar todos los supervisord activos
pkill -f "supervisord -c .*supervisor_simulador.conf"

# bash /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/scripts/ports_stop.sh


# Limpiar sockets y pids viejos
rm -f /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/logs/supervisord.sock
rm -f /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/logs/supervisord.pid

echo "✅ Limpieza hecha."

# Activar entorno y relanzar
source /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/venv/bin/activate

echo "🚀 Lanzando supervisord limpio..."
supervisord -c /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/config/supervisor_simulador.conf

sleep 5
supervisorctl -c /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/config/supervisor_simulador.conf restart gunicorn
sleep 5

supervisorctl -c /home/markmur88/api_bank_h2/scripts/utils/simulator_bank/config/supervisor_simulador.conf status

