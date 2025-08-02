#!/bin/bash

# Script para subir toda la carpeta elizaos_completo al VPS
echo "📤 Subiendo ElizaOS Completo al VPS..."

# Verificar que existe la carpeta
if [ ! -d "elizaos_completo" ]; then
    echo "❌ Error: No se encuentra la carpeta elizaos_completo"
    echo "Asegúrate de estar en el directorio correcto"
    exit 1
fi

# Verificar que existe la clave SSH
if [ ! -f "vps_njalla_nueva" ]; then
    echo "❌ Error: No se encuentra la clave SSH vps_njalla_nueva"
    exit 1
fi

echo "📁 Creando directorio en el VPS..."
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "mkdir -p ~/elizaos_completo"

echo "📤 Subiendo archivos..."
scp -i vps_njalla_nueva -r elizaos_completo/* markmur88@80.78.30.242:~/elizaos_completo/

echo "📤 Subiendo carpeta agentes_elizaos..."
scp -i vps_njalla_nueva -r agentes_elizaos markmur88@80.78.30.242:~/elizaos_completo/

echo "🔧 Configurando permisos..."
ssh -i vps_njalla_nueva markmur88@80.78.30.242 << 'EOF'
cd ~/elizaos_completo
chmod +x scripts/*.sh
chmod +x agentes_elizaos/scripts/*.sh
echo "✅ Permisos configurados"
EOF

echo "📋 Verificando archivos subidos..."
ssh -i vps_njalla_nueva markmur88@80.78.30.242 << 'EOF'
echo "📁 Estructura de archivos en el VPS:"
cd ~/elizaos_completo
echo "📄 Archivos principales:"
ls -la
echo ""
echo "📁 Configuraciones:"
ls -la configs/
echo ""
echo "📁 Scripts:"
ls -la scripts/
echo ""
echo "📁 Sistema de Agentes:"
ls -la agentes_elizaos/
EOF

echo ""
echo "🎉 ¡Subida completada!"
echo "📁 Ubicación en el VPS: ~/elizaos_completo/"
echo ""
echo "🚀 Para usar los scripts:"
echo "   ssh -i vps_njalla_nueva markmur88@80.78.30.242"
echo "   cd ~/elizaos_completo"
echo ""
echo "📋 Scripts disponibles:"
echo "   - scripts/instalar_elizaos.sh"
echo "   - scripts/configurar_elizaos.sh"
echo "   - scripts/configurar_version_completa.sh"
echo "   - scripts/crear_agente_completo.sh"
echo "   - agentes_elizaos/scripts/levantar_sistema_completo.sh"
echo "   - agentes_elizaos/scripts/diagnostico_completo.sh" 