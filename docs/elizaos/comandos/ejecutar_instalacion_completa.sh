#!/bin/bash

# Script para ejecutar la instalación completa de ElizaOS
echo "🚀 INSTALACIÓN COMPLETA DE ELIZAOS"
echo "=================================="

echo "📋 Verificando archivos necesarios..."

# Verificar que existe la carpeta elizaos_completo
if [ ! -d "elizaos_completo" ]; then
    echo "❌ Error: No se encuentra la carpeta elizaos_completo"
    exit 1
fi

# Verificar que existe la carpeta agentes_elizaos
if [ ! -d "agentes_elizaos" ]; then
    echo "❌ Error: No se encuentra la carpeta agentes_elizaos"
    exit 1
fi

# Verificar que existe la clave SSH
if [ ! -f "vps_njalla_nueva" ]; then
    echo "❌ Error: No se encuentra la clave SSH vps_njalla_nueva"
    exit 1
fi

echo "✅ Archivos verificados"

echo ""
echo "📤 1. SUBIENDO ARCHIVOS AL VPS"
echo "-----------------------------"
./subir_elizaos_completo.sh

echo ""
echo "🔧 2. EJECUTANDO INSTALACIÓN EN EL VPS"
echo "-------------------------------------"
echo "Conectando al VPS y ejecutando instalación..."
ssh -i vps_njalla_nueva markmur88@80.78.30.242 << 'EOF'
cd ~/elizaos_completo
chmod +x scripts/*.sh
chmod +x agentes_elizaos/scripts/*.sh
./scripts/instalacion_completa.sh
EOF

echo ""
echo "🎉 ¡INSTALACIÓN COMPLETADA!"
echo "=========================="
echo ""
echo "🌐 URLs de acceso:"
echo "   - ElizaOS Básico: http://amara.coretransapi.com:9182"
echo "   - Agente Completo: http://amara.coretransapi.com:9190"
echo "   - Agentes Especializados: http://amara.coretransapi.com:9183-9187"
echo ""
echo "📋 Para verificar el estado:"
echo "   ssh -i vps_njalla_nueva markmur88@80.78.30.242"
echo "   cd ~/elizaos_completo"
echo "   ./agentes_elizaos/scripts/diagnostico_completo.sh"
echo ""
echo "✅ ¡ElizaOS está completamente instalado y funcionando!" 