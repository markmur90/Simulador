# Script para solucionar el problema del bucle infinito de ElizaOS
Write-Host "Solucionando problema de ElizaOS..." -ForegroundColor Green

Write-Host "1. Deteniendo procesos problemáticos..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 stop all 2>/dev/null || true && pm2 delete all 2>/dev/null || true"

Write-Host "2. Verificando configuración..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "cd ~/eliza-develop && cat .env && echo 'Configuración del agente:' && cat .eliza/agents/amara-complete/config.json | grep -A 5 -B 5 port"

Write-Host "3. Iniciando agente correctamente..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "cd ~/eliza-develop && source ~/.zshrc && cd packages/cli && pm2 start dist/index.js --name 'amara-complete' -- start"

Write-Host "4. Verificando estado..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "sleep 5 && pm2 list && echo 'Puertos en uso:' && netstat -tlnp | grep -E ':(918[2-7]|919[0-1])'"

Write-Host "5. Verificando logs..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 logs amara-complete --lines 5"

Write-Host "Solucion completada!" -ForegroundColor Green 