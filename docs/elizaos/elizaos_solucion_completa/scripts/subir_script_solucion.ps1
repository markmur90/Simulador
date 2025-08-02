# Script para subir el script de solución al VPS
Write-Host "Subiendo script de solución al VPS..." -ForegroundColor Green

# Verificar que existe el script
if (-not (Test-Path "solucion_manual_elizaos.sh")) {
    Write-Host "Error: No se encuentra el script solucion_manual_elizaos.sh" -ForegroundColor Red
    exit 1
}

# Verificar que existe la clave SSH
if (-not (Test-Path "vps_njalla_nueva")) {
    Write-Host "Error: No se encuentra la clave SSH vps_njalla_nueva" -ForegroundColor Red
    exit 1
}

Write-Host "Subiendo script..." -ForegroundColor Yellow
scp -i vps_njalla_nueva solucion_manual_elizaos.sh markmur88@80.78.30.242:~/

Write-Host "Configurando permisos..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "chmod +x ~/solucion_manual_elizaos.sh"

Write-Host "Verificando archivo..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "ls -la ~/solucion_manual_elizaos.sh"

Write-Host ""
Write-Host "Script subido correctamente!" -ForegroundColor Green
Write-Host "Para ejecutar en el VPS:" -ForegroundColor Yellow
Write-Host "  ssh -i vps_njalla_nueva markmur88@80.78.30.242" -ForegroundColor White
Write-Host "  ./solucion_manual_elizaos.sh" -ForegroundColor White 