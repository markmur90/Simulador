@echo off
REM =====================================
REM CONFIGURAR SSH SIN CONTRASEÑA
REM =====================================

echo 🔧 Configurando SSH sin contraseña...
echo.

REM Verificar archivos SSH
if not exist "vps_njalla_nueva" (
    echo ❌ Error: No se encuentra vps_njalla_nueva
    pause
    exit /b 1
)

if not exist "vps_njalla_nueva.pub" (
    echo ❌ Error: No se encuentra vps_njalla_nueva.pub
    pause
    exit /b 1
)

echo ✅ Archivos SSH encontrados

REM Configurar permisos
echo 🔐 Configurando permisos...
icacls vps_njalla_nueva /inheritance:r /grant:r "%USERNAME%:F" >nul 2>&1
echo ✅ Permisos configurados

REM Crear directorio .ssh
echo 📁 Creando directorio .ssh...
mkdir "%USERPROFILE%\.ssh" 2>nul
echo ✅ Directorio .ssh creado

REM Crear configuración SSH
echo ⚙️ Configurando SSH config...
(
echo Host vps-elizaos
echo     HostName 80.78.30.242
echo     User markmur88
echo     IdentityFile "%cd%\vps_njalla_nueva"
echo     IdentitiesOnly yes
echo     StrictHostKeyChecking no
echo     ServerAliveInterval 60
echo     ServerAliveCountMax 3
echo     ConnectTimeout 30
) > "%USERPROFILE%\.ssh\config"

echo ✅ SSH config creado

REM Probar conexión
echo 🧪 Probando conexión SSH...
ssh -o ConnectTimeout=10 vps-elizaos "echo 'Conexión SSH exitosa sin contraseña'" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Conexión SSH configurada correctamente
    echo.
    echo 🎉 ¡Configuración completada!
    echo.
    echo 💡 Ahora puedes usar:
    echo    ssh vps-elizaos
    echo    conectar_vps_simple.bat
) else (
    echo ⚠️ La conexión SSH aún puede pedir contraseña
    echo 💡 Esto es normal en la primera conexión
)

echo.
pause 