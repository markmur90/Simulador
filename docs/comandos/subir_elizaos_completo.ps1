# Script de PowerShell para subir ElizaOS Completo al VPS
Write-Host "📤 Subiendo ElizaOS Completo al VPS..." -ForegroundColor Green

# Verificar que existe la carpeta
if (-not (Test-Path "elizaos_completo")) {
    Write-Host "❌ Error: No se encuentra la carpeta elizaos_completo" -ForegroundColor Red
    Write-Host "Asegúrate de estar en el directorio correcto" -ForegroundColor Yellow
    exit 1
}

# Verificar que existe la clave SSH
if (-not (Test-Path "vps_njalla_nueva")) {
    Write-Host "❌ Error: No se encuentra la clave SSH vps_njalla_nueva" -ForegroundColor Red
    exit 1
}

Write-Host "📁 Creando directorio en el VPS..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "mkdir -p ~/elizaos_completo"

Write-Host "📤 Subiendo archivos..." -ForegroundColor Yellow
scp -i vps_njalla_nueva -r elizaos_completo/* markmur88@80.78.30.242:~/elizaos_completo/

Write-Host "📤 Subiendo carpeta agentes_elizaos..." -ForegroundColor Yellow
scp -i vps_njalla_nueva -r agentes_elizaos markmur88@80.78.30.242:~/elizaos_completo/

Write-Host "🔧 Configurando permisos..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 @"
cd ~/elizaos_completo
chmod +x scripts/*.sh
chmod +x agentes_elizaos/scripts/*.sh
echo '✅ Permisos configurados'
"@

Write-Host "📋 Verificando archivos subidos..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 @"
echo '📁 Estructura de archivos en el VPS:'
cd ~/elizaos_completo
echo '📄 Archivos principales:'
ls -la
echo ''
echo '📁 Configuraciones:'
ls -la configs/
echo ''
echo '📁 Scripts:'
ls -la scripts/
echo ''
echo '📁 Sistema de Agentes:'
ls -la agentes_elizaos/
"@

Write-Host ""
Write-Host "🎉 ¡Subida completada!" -ForegroundColor Green
Write-Host "📁 Ubicación en el VPS: ~/elizaos_completo/" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Para usar los scripts:" -ForegroundColor Yellow
Write-Host "   ssh -i vps_njalla_nueva markmur88@80.78.30.242" -ForegroundColor White
Write-Host "   cd ~/elizaos_completo" -ForegroundColor White
Write-Host ""
Write-Host "📋 Scripts disponibles:" -ForegroundColor Yellow
Write-Host "   - scripts/instalar_elizaos.sh" -ForegroundColor White
Write-Host "   - scripts/configurar_elizaos.sh" -ForegroundColor White
Write-Host "   - scripts/configurar_version_completa.sh" -ForegroundColor White
Write-Host "   - scripts/crear_agente_completo.sh" -ForegroundColor White
Write-Host "   - agentes_elizaos/scripts/levantar_sistema_completo.sh" -ForegroundColor White
Write-Host "   - agentes_elizaos/scripts/diagnostico_completo.sh" -ForegroundColor White 