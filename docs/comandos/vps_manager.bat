@echo off
REM =====================================
REM GESTOR DE VPS ELIZAOS PARA WINDOWS
REM =====================================
REM Autor: Sistema ElizaOS
REM Versión: 1.0
REM Descripción: Script batch para ejecutar el gestor de VPS en Windows

setlocal enabledelayedexpansion

REM Configuración
set VPS_IP=80.78.30.242
set VPS_USER=markmur88
set SSH_KEY=vps_njalla_nueva

REM Colores (Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "NC=[0m"

REM Función para mostrar banner
:show_banner
cls
echo %CYAN%
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                GESTOR DE VPS ELIZAOS - WINDOWS               ║
echo ║                    Sistema de Administración                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo %NC%
echo %YELLOW%VPS: %VPS_USER%@%VPS_IP%%NC%
echo %YELLOW%Clave SSH: %SSH_KEY%%NC%
echo.

REM Verificar si Git Bash está disponible
where bash >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%❌ Error: Git Bash no está disponible%NC%
    echo %YELLOW%Por favor instala Git for Windows desde: https://git-scm.com/download/win%NC%
    echo.
    echo %CYAN%Alternativas:%NC%
    echo %YELLOW%1. Usar WSL (Windows Subsystem for Linux)%NC%
    echo %YELLOW%2. Usar PowerShell con OpenSSH%NC%
    echo %YELLOW%3. Usar PuTTY para conexiones SSH%NC%
    pause
    exit /b 1
)

REM Verificar archivos SSH
if not exist "%SSH_KEY%" (
    echo %RED%❌ Error: No se encuentra la clave SSH %SSH_KEY%%NC%
    echo %YELLOW%Asegúrate de que el archivo esté en el directorio actual%NC%
    pause
    exit /b 1
)

if not exist "%SSH_KEY%.pub" (
    echo %RED%❌ Error: No se encuentra la clave pública %SSH_KEY%.pub%NC%
    echo %YELLOW%Asegúrate de que el archivo esté en el directorio actual%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Archivos SSH encontrados%NC%
echo.

REM Mostrar menú
:show_menu
echo %CYAN%
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                        MENÚ PRINCIPAL                        ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║ 🔌 CONEXIÓN:                                                ║
echo ║   1. Conectar al VPS (SSH interactivo)                      ║
echo ║   2. Verificar conectividad                                 ║
echo ║                                                              ║
echo ║ 📊 GESTIÓN:                                                 ║
echo ║   3. Mostrar estado del VPS                                 ║
echo ║   4. Reiniciar servicios ElizaOS                            ║
echo ║   5. Crear backup                                           ║
echo ║   6. Mostrar logs                                           ║
echo ║                                                              ║
echo ║ 📁 TRANSFERENCIA:                                           ║
echo ║   7. Subir archivos                                         ║
echo ║   8. Descargar archivos                                     ║
echo ║                                                              ║
echo ║ ⚙️ CONFIGURACIÓN:                                           ║
echo ║   9. Configurar SSH                                         ║
echo ║   10. Mostrar información de configuración                  ║
echo ║                                                              ║
echo ║ 0. 🚪 Salir                                                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo %NC%

echo %YELLOW%Selecciona una opción:%NC%
set /p option="> "

echo.

REM Manejar opciones
if "%option%"=="1" goto connect_ssh
if "%option%"=="2" goto check_connectivity
if "%option%"=="3" goto show_status
if "%option%"=="4" goto restart_services
if "%option%"=="5" goto create_backup
if "%option%"=="6" goto show_logs
if "%option%"=="7" goto upload_files
if "%option%"=="8" goto download_files
if "%option%"=="9" goto setup_ssh
if "%option%"=="10" goto show_info
if "%option%"=="0" goto exit_script
goto invalid_option

REM Conectar SSH
:connect_ssh
echo %BLUE%🔌 Conectando al VPS...%NC%
echo %GREEN%🚀 Conectando a %VPS_USER%@%VPS_IP%...%NC%
echo %CYAN%💡 Usa 'exit' para salir%NC%
echo.
bash -c "ssh -i '%SSH_KEY%' -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ConnectTimeout=30 -o StrictHostKeyChecking=no '%VPS_USER%@%VPS_IP%'"
goto continue

REM Verificar conectividad
:check_connectivity
echo %BLUE%🔍 Verificando conectividad al VPS...%NC%
ping -n 1 -w 5000 %VPS_IP% >nul 2>&1
if %errorlevel% equ 0 (
    echo %GREEN%✅ VPS responde al ping%NC%
) else (
    echo %RED%❌ VPS no responde al ping%NC%
)
goto continue

REM Mostrar estado
:show_status
echo %BLUE%📊 Estado del VPS...%NC%
bash -c "ssh -i '%SSH_KEY%' -o ConnectTimeout=30 -o StrictHostKeyChecking=no '%VPS_USER%@%VPS_IP%' 'echo \"=== INFORMACIÓN DEL SISTEMA ===\" && hostname && uptime -p && free -h && df -h / && echo \"\" && echo \"=== SERVICIOS ELIZAOS ===\" && cd ~/elizaos_completo 2>/dev/null && ls -la || echo \"Directorio no encontrado\"'"
goto continue

REM Reiniciar servicios
:restart_services
echo %BLUE%🔄 Reiniciando servicios ElizaOS...%NC%
bash -c "ssh -i '%SSH_KEY%' -o ConnectTimeout=30 -o StrictHostKeyChecking=no '%VPS_USER%@%VPS_IP%' 'cd ~/elizaos_completo && pkill -f elizaos || true && pkill -f agente || true && sleep 2 && chmod +x scripts/levantar_sistema_completo.sh 2>/dev/null && ./scripts/levantar_sistema_completo.sh || echo \"Script no encontrado\"'"
goto continue

REM Crear backup
:create_backup
echo %BLUE%💾 Creando backup...%NC%
bash -c "ssh -i '%SSH_KEY%' -o ConnectTimeout=30 -o StrictHostKeyChecking=no '%VPS_USER%@%VPS_IP%' 'cd ~ && mkdir -p backups && tar -czf backups/elizaos_backup_$(date +%%Y%%m%%d_%%H%%M%%S).tar.gz elizaos_completo/ && echo \"Backup creado\"'"
goto continue

REM Mostrar logs
:show_logs
echo %BLUE%📋 Mostrando logs recientes...%NC%
bash -c "ssh -i '%SSH_KEY%' -o ConnectTimeout=30 -o StrictHostKeyChecking=no '%VPS_USER%@%VPS_IP%' 'journalctl --since \"1 hour ago\" | grep -i elizaos | tail -20'"
goto continue

REM Subir archivos
:upload_files
echo %YELLOW%📤 Ingresa la ruta del archivo/carpeta a subir:%NC%
set /p source_path="> "
if exist "%source_path%" (
    echo %BLUE%📤 Subiendo archivos...%NC%
    bash -c "scp -i '%SSH_KEY%' -o ConnectTimeout=30 -o StrictHostKeyChecking=no -r '%source_path%' '%VPS_USER%@%VPS_IP%:~/elizaos_completo/'"
    echo %GREEN%✅ Archivos subidos correctamente%NC%
) else (
    echo %RED%❌ Ruta inválida o archivo no existe%NC%
)
goto continue

REM Descargar archivos
:download_files
echo %YELLOW%📥 Ingresa la ruta del archivo/carpeta a descargar:%NC%
set /p source_path="> "
if not "%source_path%"=="" (
    echo %BLUE%📥 Descargando archivos...%NC%
    bash -c "scp -i '%SSH_KEY%' -o ConnectTimeout=30 -o StrictHostKeyChecking=no -r '%VPS_USER%@%VPS_IP%:%source_path%' ."
    echo %GREEN%✅ Archivos descargados correctamente%NC%
) else (
    echo %RED%❌ Ruta inválida%NC%
)
goto continue

REM Configurar SSH
:setup_ssh
echo %BLUE%⚙️ Configurando SSH...%NC%
echo %YELLOW%⚠️ Esta función requiere configuración manual en Windows%NC%
echo %CYAN%Pasos recomendados:%NC%
echo %YELLOW%1. Instalar Git for Windows%NC%
echo %YELLOW%2. Configurar SSH config en %USERPROFILE%\.ssh\config%NC%
echo %YELLOW%3. Usar PuTTY o Git Bash para conexiones SSH%NC%
goto continue

REM Mostrar información
:show_info
echo %CYAN%📊 INFORMACIÓN DE CONFIGURACIÓN%NC%
echo ==================================
echo %YELLOW%VPS IP: %VPS_IP%%NC%
echo %YELLOW%Usuario: %VPS_USER%%NC%
echo %YELLOW%Clave SSH: %SSH_KEY%%NC%
echo.
echo %GREEN%🚀 Comandos disponibles:%NC%
echo %CYAN%  bash -c "ssh -i '%SSH_KEY%' '%VPS_USER%@%VPS_IP%'"%NC% - Conectar al VPS
echo %CYAN%  bash -c "scp -i '%SSH_KEY%' archivo '%VPS_USER%@%VPS_IP%:~/'"%NC% - Subir archivo
echo %CYAN%  bash -c "scp -i '%SSH_KEY%' '%VPS_USER%@%VPS_IP%:~/archivo' ."%NC% - Descargar archivo
echo.
goto continue

REM Opción inválida
:invalid_option
echo %RED%❌ Opción inválida%NC%
goto continue

REM Continuar
:continue
echo.
echo %CYAN%Presiona Enter para continuar...%NC%
pause >nul
goto show_menu

REM Salir
:exit_script
echo %GREEN%👋 ¡Hasta luego!%NC%
exit /b 0 