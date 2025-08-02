#!/bin/bash

echo "🔧 SOLUCIONANDO PROBLEMA DE ELIZAOS"
echo "===================================="

echo "1. Deteniendo procesos problemáticos..."
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true

echo "2. Verificando configuración..."
cd ~/eliza-develop
echo "Variables de entorno:"
cat .env
echo ""
echo "Configuración del agente:"
cat .eliza/agents/amara-complete/config.json | grep -A 5 -B 5 port

echo "3. Iniciando agente correctamente..."
source ~/.zshrc
cd packages/cli
pm2 start dist/index.js --name 'amara-complete' -- start

echo "4. Esperando 5 segundos..."
sleep 5

echo "5. Verificando estado..."
pm2 list

echo "6. Verificando puertos..."
netstat -tlnp | grep -E ':(918[2-7]|919[0-1])'

echo "7. Verificando logs..."
pm2 logs amara-complete --lines 5

echo ""
echo "🎉 ¡SOLUCIÓN COMPLETADA!"
echo "========================"
echo ""
echo "🌐 URLs de acceso:"
echo "   - http://amara.coretransapi.com:9190"
echo "   - http://80.78.30.242:9190"
echo ""
echo "📋 Para verificar logs:"
echo "   pm2 logs amara-complete"
echo ""
echo "📋 Para reiniciar:"
echo "   pm2 restart amara-complete" 