# Script para ejecutar la solución completa de ElizaOS
Write-Host "Ejecutando solución completa de ElizaOS..." -ForegroundColor Green

# Verificar que existe el script
if (-not (Test-Path "solucionar_base_datos.sh")) {
    Write-Host "Error: No se encuentra el script solucionar_base_datos.sh" -ForegroundColor Red
    exit 1
}

# Verificar que existe la clave SSH
if (-not (Test-Path "vps_njalla_nueva")) {
    Write-Host "Error: No se encuentra la clave SSH vps_njalla_nueva" -ForegroundColor Red
    exit 1
}

Write-Host "1. Subiendo script de solución..." -ForegroundColor Yellow
scp -i vps_njalla_nueva solucionar_base_datos.sh markmur88@80.78.30.242:~/

Write-Host "2. Configurando permisos..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "chmod +x ~/solucionar_base_datos.sh"

Write-Host "3. Verificando archivo..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "ls -la ~/solucionar_base_datos.sh"

Write-Host "4. Ejecutando solución..." -ForegroundColor Yellow
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "./solucionar_base_datos.sh"

Write-Host ""
Write-Host "Solución completada!" -ForegroundColor Green
Write-Host "ElizaOS debería estar funcionando en:" -ForegroundColor Yellow
Write-Host "  - http://amara.coretransapi.com:9190" -ForegroundColor White
Write-Host "  - http://80.78.30.242:9190" -ForegroundColor White 