@echo off
echo Solucionando ElizaOS...

echo 1. Deteniendo procesos...
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 stop all"
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 delete all"

echo 2. Iniciando agente correctamente...
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "cd ~/eliza-develop && source ~/.zshrc && cd packages/cli && pm2 start dist/index.js --name 'amara-complete' -- start"

echo 3. Verificando estado...
timeout /t 5
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 list"

echo 4. Verificando puertos...
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "netstat -tlnp | grep -E ':(918[2-7]|919[0-1])'"

echo Completado!
pause 