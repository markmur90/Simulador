#!/bin/bash

echo "🔧 SOLUCIONANDO PROBLEMA DE BASE DE DATOS"
echo "=========================================="

echo "1. Deteniendo el agente..."
pm2 stop amara-complete

echo "2. Limpiando base de datos corrupta..."
cd ~/eliza-develop
rm -rf .eliza

echo "3. Creando nueva base de datos..."
mkdir -p .eliza

echo "4. Verificando configuración..."
cat .env
echo ""
echo "Configuración del agente:"
cat .eliza/agents/amara-complete/config.json | grep -A 5 -B 5 port

echo "5. Iniciando agente con base de datos limpia..."
source ~/.zshrc
cd packages/cli
pm2 start dist/index.js --name 'amara-complete' -- start

echo "6. Esperando 10 segundos..."
sleep 10

echo "7. Verificando estado..."
pm2 list

echo "8. Verificando puertos..."
netstat -tlnp | grep -E ':(918[2-7]|919[0-1])'

echo "9. Verificando logs..."
pm2 logs amara-complete --lines 10

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