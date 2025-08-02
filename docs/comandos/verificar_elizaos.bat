@echo off
REM =====================================
REM VERIFICAR ESTADO DE ELIZAOS
REM =====================================

echo 🔍 Verificando estado de ElizaOS...
echo.

REM Verificar conectividad
echo 📡 Verificando conectividad...
ping -n 1 80.78.30.242 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ VPS responde al ping
) else (
    echo ❌ VPS no responde al ping
    pause
    exit /b 1
)

echo.
echo 🚀 Conectando al VPS para verificar ElizaOS...
echo.

REM Conectar y verificar ElizaOS
ssh -i vps_njalla_nueva -o ConnectTimeout=30 -o StrictHostKeyChecking=no markmur88@80.78.30.242 "echo '=== ESTADO DE ELIZAOS ===' && echo '1. Procesos ElizaOS:' && ps aux | grep -i eliza | grep -v grep | head -5 && echo '' && echo '2. Puertos en uso:' && netstat -tlnp | grep -E ':(918[0-9]|919[0-9])' | head -5 && echo '' && echo '3. Directorios ElizaOS:' && find /home/markmur88 -name '*eliza*' -type d 2>/dev/null | head -5"

echo.
echo ✅ Verificación completada
pause 