# 🪟 ElizaOS - Guía Completa para Windows

## 📋 Requisitos Previos

### Software Necesario
- **Windows 10/11** (64-bit)
- **PowerShell 5.1+** (incluido en Windows 10/11)
- **Git Bash** o **WSL** (opcional, para comandos bash)
- **PuTTY** o **OpenSSH** (para conexión SSH)

### Verificar PowerShell
```powershell
# Verificar versión de PowerShell
$PSVersionTable.PSVersion

# Si es menor a 5.1, actualizar Windows
```

### Instalar OpenSSH (si no está disponible)
```powershell
# Como administrador
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

## 🚀 Instalación en Windows

### Paso 1: Preparar el Entorno
```powershell
# Navegar al directorio del proyecto
cd C:\projects\Simulador\docs\elizaos

# Verificar que estamos en el directorio correcto
dir
```

### Paso 2: Organizar Archivos
```powershell
# Ejecutar script de organización
cd comandos
.\organizar_elizaos.ps1
```

Este script:
- ✅ Crea la carpeta `elizaos_solucion_completa`
- ✅ Organiza todos los archivos en subcarpetas
- ✅ Genera documentación automática
- ✅ Verifica la estructura del proyecto

### Paso 3: Subir Archivos al VPS
```powershell
# Subir archivos completos
.\subir_elizaos_completo.ps1
```

Este script:
- ✅ Conecta al VPS automáticamente
- ✅ Sube todos los archivos necesarios
- ✅ Configura permisos de ejecución
- ✅ Verifica la transferencia

## 🔧 Scripts de Windows Disponibles

### Scripts Principales
```powershell
# Organizar proyecto
.\organizar_elizaos.ps1

# Subir archivos completos
.\subir_elizaos_completo.ps1

# Subir archivos simples
.\subir_elizaos_simple.ps1

# Ejecutar solución completa
.\ejecutar_solucion_completa.ps1

# Subir script de solución
.\subir_script_solucion.ps1

# Solucionar problemas
.\solucionar_elizaos.ps1
```

### Scripts de Batch (.bat)
```cmd
# Reiniciar ElizaOS simple
reiniciar_elizaos_simple.bat

# Verificar estado
verificar_elizaos.bat

# Conectar al VPS
conectar_vps_simple.bat

# Configurar SSH sin password
configurar_ssh_sin_password.bat

# Gestor de VPS completo
vps_manager.bat
```

## 🌐 Conexión al VPS

### Método 1: PowerShell (Recomendado)
```powershell
# Conectar usando la clave SSH
ssh -i vps_njalla_nueva markmur88@80.78.30.242
```

### Método 2: Script Automático
```powershell
# Usar script de conexión
.\conectar_vps_simple.bat
```

### Método 3: PuTTY
1. Abrir PuTTY
2. Host: `80.78.30.242`
3. Puerto: `22`
4. Usuario: `markmur88`
5. Cargar clave privada en Connection > SSH > Auth

## 📋 Flujo de Trabajo Completo

### 1. Preparación Local (Windows)
```powershell
# Navegar al directorio
cd C:\projects\Simulador\docs\elizaos\comandos

# Organizar archivos
.\organizar_elizaos.ps1

# Subir al VPS
.\subir_elizaos_completo.ps1
```

### 2. Instalación en VPS
```powershell
# Conectar al VPS
ssh -i vps_njalla_nueva markmur88@80.78.30.242

# En el VPS, ejecutar:
cd ~/elizaos_completo
./scripts/instalacion_completa.sh
```

### 3. Verificación
```powershell
# Verificar estado desde Windows
.\verificar_elizaos.bat

# O conectar y verificar manualmente
ssh -i vps_njalla_nueva markmur88@80.78.30.242
pm2 list
```

## 🛠️ Troubleshooting en Windows

### Problema: PowerShell Execution Policy
```powershell
# Error: "Execution policy prevents running scripts"
# Solución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema: SSH Connection Refused
```powershell
# Verificar conectividad
Test-NetConnection -ComputerName 80.78.30.242 -Port 22

# Verificar clave SSH
ssh -i vps_njalla_nueva -o ConnectTimeout=10 markmur88@80.78.30.242
```

### Problema: Archivos No Encontrados
```powershell
# Verificar estructura
Get-ChildItem -Recurse -Name

# Verificar permisos
Get-Acl vps_njalla_nueva
```

### Problema: Scripts No Ejecutan
```powershell
# Verificar permisos de scripts
Get-ChildItem *.ps1 | Get-Acl

# Ejecutar como administrador si es necesario
Start-Process PowerShell -Verb RunAs
```

## 📊 Monitoreo desde Windows

### Verificar Estado del VPS
```powershell
# Script de verificación
.\verificar_elizaos.bat

# Verificar puertos
Test-NetConnection -ComputerName amara.coretransapi.com -Port 9190
```

### Ver Logs Remotos
```powershell
# Conectar y ver logs
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 logs amara-complete --lines 10"
```

### Reiniciar Servicios
```powershell
# Reinicio remoto
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 restart all"
```

## 🔧 Configuración Avanzada

### Variables de Entorno en Windows
```powershell
# Configurar variables de entorno
$env:ELIZAOS_VPS_IP = "80.78.30.242"
$env:ELIZAOS_VPS_USER = "markmur88"
$env:ELIZAOS_SSH_KEY = "vps_njalla_nueva"

# Hacer permanentes
[Environment]::SetEnvironmentVariable("ELIZAOS_VPS_IP", "80.78.30.242", "User")
```

### Configurar SSH Config
```powershell
# Crear archivo de configuración SSH
$sshConfig = @"
Host elizaos-vps
    HostName 80.78.30.242
    User markmur88
    IdentityFile ~/.ssh/vps_njalla_nueva
    Port 22
"@

$sshConfig | Out-File -FilePath "$env:USERPROFILE\.ssh\config" -Encoding UTF8
```

### Alias de PowerShell
```powershell
# Crear alias útiles
Set-Alias -Name elizaos -Value "ssh -i vps_njalla_nueva markmur88@80.78.30.242"
Set-Alias -Name elizaos-status -Value ".\verificar_elizaos.bat"
```

## 🎯 Casos de Uso Específicos

### Desarrollo Local
```powershell
# Trabajar en archivos localmente
cd C:\projects\Simulador\docs\elizaos

# Editar configuraciones
notepad elizaos_completo\configs\agente_completo.json

# Subir cambios
.\comandos\subir_elizaos_completo.ps1
```

### Mantenimiento Regular
```powershell
# Verificar estado diario
.\comandos\verificar_elizaos.bat

# Reiniciar si es necesario
.\comandos\reiniciar_elizaos_simple.bat

# Ver logs de errores
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 logs --err"
```

### Solución de Problemas
```powershell
# Diagnóstico completo
.\comandos\solucionar_elizaos.ps1

# Subir script de solución
.\comandos\subir_script_solucion.ps1

# Ejecutar solución en VPS
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "cd ~/elizaos_completo && ./scripts/solucionar_base_datos.sh"
```

## 📚 Recursos Adicionales

### Documentación
- **[README.md](README.md)** - Documentación general del proyecto
- **[comandos/README_VPS_SCRIPTS.md](comandos/README_VPS_SCRIPTS.md)** - Documentación de scripts
- **[comandos/comandos_manuales_vps.txt](comandos/comandos_manuales_vps.txt)** - Comandos manuales

### URLs de Acceso
- **Agente Principal**: http://amara.coretransapi.com:9190
- **Agente Básico**: http://amara.coretransapi.com:9182
- **Agentes Especializados**: http://amara.coretransapi.com:9183-9187

### Comandos Útiles
```powershell
# Ver todos los scripts disponibles
Get-ChildItem *.ps1, *.bat | Select-Object Name, Length, LastWriteTime

# Ver contenido de un script
Get-Content .\organizar_elizaos.ps1

# Ejecutar con parámetros
.\vps_manager.bat --help
```

## 🔒 Seguridad en Windows

### Protección de Claves SSH
```powershell
# Configurar permisos correctos
icacls vps_njalla_nueva /inheritance:r
icacls vps_njalla_nueva /grant:r "%USERNAME%:F"
```

### Firewall de Windows
```powershell
# Verificar reglas de firewall
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*SSH*"}

# Crear regla para SSH si es necesario
New-NetFirewallRule -DisplayName "SSH Outbound" -Direction Outbound -Protocol TCP -LocalPort Any -RemotePort 22 -Action Allow
```

## 📈 Optimización de Rendimiento

### Configuración de PowerShell
```powershell
# Optimizar PowerShell
$PSDefaultParameterValues['Out-Default:OutVariable'] = 'LastResult'
$PSDefaultParameterValues['*:Verbose'] = $true

# Configurar historial
$MaximumHistoryCount = 1000
```

### Configuración de SSH
```powershell
# Optimizar conexiones SSH
$sshConfig = @"
Host elizaos-vps
    HostName 80.78.30.242
    User markmur88
    IdentityFile ~/.ssh/vps_njalla_nueva
    Port 22
    Compression yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
"@
```

---

## 🎉 ¡ElizaOS en Windows está Listo!

Con esta configuración tienes:
- ✅ Scripts automatizados para Windows
- ✅ Conexión SSH simplificada
- ✅ Monitoreo remoto desde Windows
- ✅ Solución de problemas integrada
- ✅ Documentación específica para Windows

**¡Tu sistema ElizaOS está completamente configurado para Windows y listo para usar!** 