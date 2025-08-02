# 🐧 ElizaOS - Guía Completa para Linux

## 📋 Requisitos Previos

### Software Necesario
- **Ubuntu 20.04+** / **Debian 11+** / **CentOS 8+**
- **Bash 4.4+**
- **OpenSSH Client**
- **Git** (opcional, para clonar repositorios)

### Verificar Sistema
```bash
# Verificar versión de bash
bash --version

# Verificar OpenSSH
ssh -V

# Verificar sistema operativo
cat /etc/os-release
```

### Instalar Dependencias
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y openssh-client git curl wget

# CentOS/RHEL
sudo yum install -y openssh-clients git curl wget

# Arch Linux
sudo pacman -S openssh git curl wget
```

## 🚀 Instalación en Linux

### Paso 1: Preparar el Entorno
```bash
# Navegar al directorio del proyecto
cd /path/to/elizaos

# Verificar que estamos en el directorio correcto
ls -la
```

### Paso 2: Configurar Permisos
```bash
# Dar permisos de ejecución a todos los scripts
chmod +x comandos/*.sh
chmod +x elizaos_completo/scripts/*.sh
chmod +x agentes_elizaos/scripts/*.sh

# Configurar permisos de la clave SSH
chmod 600 comandos/vps_njalla_nueva
```

### Paso 3: Organizar Archivos
```bash
# Ejecutar script de organización
cd comandos
./organizar_elizaos.sh
```

Este script:
- ✅ Crea la carpeta `elizaos_solucion_completa`
- ✅ Organiza todos los archivos en subcarpetas
- ✅ Genera documentación automática
- ✅ Verifica la estructura del proyecto

### Paso 4: Subir Archivos al VPS
```bash
# Subir archivos completos
./subir_elizaos_completo.sh
```

Este script:
- ✅ Conecta al VPS automáticamente
- ✅ Sube todos los archivos necesarios
- ✅ Configura permisos de ejecución
- ✅ Verifica la transferencia

## 🔧 Scripts de Linux Disponibles

### Scripts Principales
```bash
# Organizar proyecto
./organizar_elizaos.sh

# Subir archivos completos
./subir_elizaos_completo.sh

# Subir archivos simples
./subir_elizaos_simple.sh

# Ejecutar solución completa
./ejecutar_solucion_completa.sh

# Subir script de solución
./subir_script_solucion.sh

# Solucionar problemas
./solucionar_elizaos.sh
```

### Scripts de Gestión
```bash
# Gestor de VPS completo
./vps_manager.sh

# Configurar SSH
./configurar_ssh_vps.sh

# Mantener conexión
./mantener_conexion_vps.sh

# Conectar al VPS
./conectar_vps.sh
```

## 🌐 Conexión al VPS

### Método 1: SSH Directo (Recomendado)
```bash
# Conectar usando la clave SSH
ssh -i vps_njalla_nueva markmur88@80.78.30.242
```

### Método 2: Script Automático
```bash
# Usar script de conexión
./conectar_vps.sh
```

### Método 3: Configuración SSH
```bash
# Crear configuración SSH
mkdir -p ~/.ssh
cat > ~/.ssh/config << 'EOF'
Host elizaos-vps
    HostName 80.78.30.242
    User markmur88
    IdentityFile ~/.ssh/vps_njalla_nueva
    Port 22
    Compression yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
EOF

# Conectar usando alias
ssh elizaos-vps
```

## 📋 Flujo de Trabajo Completo

### 1. Preparación Local (Linux)
```bash
# Navegar al directorio
cd /path/to/elizaos/comandos

# Configurar permisos
chmod +x *.sh

# Organizar archivos
./organizar_elizaos.sh

# Subir al VPS
./subir_elizaos_completo.sh
```

### 2. Instalación en VPS
```bash
# Conectar al VPS
ssh -i vps_njalla_nueva markmur88@80.78.30.242

# En el VPS, ejecutar:
cd ~/elizaos_completo
./scripts/instalacion_completa.sh
```

### 3. Verificación
```bash
# Verificar estado desde Linux
./verificar_elizaos.sh

# O conectar y verificar manualmente
ssh -i vps_njalla_nueva markmur88@80.78.30.242
pm2 list
```

## 🛠️ Troubleshooting en Linux

### Problema: Permisos de Scripts
```bash
# Error: "Permission denied"
# Solución:
chmod +x *.sh
chmod +x elizaos_completo/scripts/*.sh
chmod +x agentes_elizaos/scripts/*.sh
```

### Problema: SSH Connection Refused
```bash
# Verificar conectividad
ping -c 3 80.78.30.242
telnet 80.78.30.242 22

# Verificar clave SSH
ssh -i vps_njalla_nueva -o ConnectTimeout=10 markmur88@80.78.30.242
```

### Problema: Archivos No Encontrados
```bash
# Verificar estructura
find . -type f -name "*.sh" -exec ls -la {} \;

# Verificar permisos
ls -la vps_njalla_nueva
```

### Problema: Dependencias Faltantes
```bash
# Instalar dependencias básicas
sudo apt update && sudo apt install -y openssh-client rsync curl wget

# Verificar instalación
which ssh
which rsync
which curl
```

## 📊 Monitoreo desde Linux

### Verificar Estado del VPS
```bash
# Script de verificación
./verificar_elizaos.sh

# Verificar puertos
nc -zv amara.coretransapi.com 9190
```

### Ver Logs Remotos
```bash
# Conectar y ver logs
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 logs amara-complete --lines 10"

# Ver logs en tiempo real
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 logs amara-complete --follow"
```

### Reiniciar Servicios
```bash
# Reinicio remoto
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 restart all"

# Reinicio específico
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 restart amara-complete"
```

## 🔧 Configuración Avanzada

### Variables de Entorno en Linux
```bash
# Configurar variables de entorno
export ELIZAOS_VPS_IP="80.78.30.242"
export ELIZAOS_VPS_USER="markmur88"
export ELIZAOS_SSH_KEY="vps_njalla_nueva"

# Hacer permanentes (añadir a ~/.bashrc)
echo 'export ELIZAOS_VPS_IP="80.78.30.242"' >> ~/.bashrc
echo 'export ELIZAOS_VPS_USER="markmur88"' >> ~/.bashrc
echo 'export ELIZAOS_SSH_KEY="vps_njalla_nueva"' >> ~/.bashrc
source ~/.bashrc
```

### Configurar Alias Útiles
```bash
# Crear alias en ~/.bashrc
echo 'alias elizaos="ssh -i vps_njalla_nueva markmur88@80.78.30.242"' >> ~/.bashrc
echo 'alias elizaos-status="./verificar_elizaos.sh"' >> ~/.bashrc
echo 'alias elizaos-logs="ssh -i vps_njalla_nueva markmur88@80.78.30.242 \"pm2 logs amara-complete --lines 20\"' >> ~/.bashrc
source ~/.bashrc
```

### Configurar rsync para Transferencias
```bash
# Crear script de sincronización
cat > sync_elizaos.sh << 'EOF'
#!/bin/bash
rsync -avz --exclude='.git' --exclude='node_modules' \
    -e "ssh -i vps_njalla_nueva" \
    ./ markmur88@80.78.30.242:~/elizaos_completo/
EOF

chmod +x sync_elizaos.sh
```

## 🎯 Casos de Uso Específicos

### Desarrollo Local
```bash
# Trabajar en archivos localmente
cd /path/to/elizaos

# Editar configuraciones
nano elizaos_completo/configs/agente_completo.json

# Subir cambios
./comandos/subir_elizaos_completo.sh
```

### Mantenimiento Regular
```bash
# Verificar estado diario
./comandos/verificar_elizaos.sh

# Reiniciar si es necesario
./comandos/reiniciar_elizaos_simple.sh

# Ver logs de errores
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "pm2 logs --err"
```

### Solución de Problemas
```bash
# Diagnóstico completo
./comandos/solucionar_elizaos.sh

# Subir script de solución
./comandos/subir_script_solucion.sh

# Ejecutar solución en VPS
ssh -i vps_njalla_nueva markmur88@80.78.30.242 "cd ~/elizaos_completo && ./scripts/solucionar_base_datos.sh"
```

### Automatización con Cron
```bash
# Crear script de monitoreo automático
cat > /home/$USER/check_elizaos.sh << 'EOF'
#!/bin/bash
cd /path/to/elizaos/comandos
./verificar_elizaos.sh > /tmp/elizaos_status.log 2>&1
EOF

chmod +x /home/$USER/check_elizaos.sh

# Añadir a crontab (verificar cada hora)
crontab -e
# Añadir línea: 0 * * * * /home/$USER/check_elizaos.sh
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
```bash
# Ver todos los scripts disponibles
find . -name "*.sh" -type f -exec ls -la {} \;

# Ver contenido de un script
cat ./organizar_elizaos.sh

# Ejecutar con parámetros
./vps_manager.sh --help

# Ver logs del sistema
journalctl -u ssh -f
```

## 🔒 Seguridad en Linux

### Protección de Claves SSH
```bash
# Configurar permisos correctos
chmod 600 vps_njalla_nueva
chmod 700 ~/.ssh

# Verificar permisos
ls -la vps_njalla_nueva
ls -ld ~/.ssh
```

### Configurar SSH Config
```bash
# Crear configuración SSH segura
cat > ~/.ssh/config << 'EOF'
Host elizaos-vps
    HostName 80.78.30.242
    User markmur88
    IdentityFile ~/.ssh/vps_njalla_nueva
    Port 22
    Compression yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
EOF

chmod 600 ~/.ssh/config
```

### Firewall Local
```bash
# Verificar UFW (si está instalado)
sudo ufw status

# Crear regla para SSH si es necesario
sudo ufw allow out 22/tcp
```

## 📈 Optimización de Rendimiento

### Configuración de Bash
```bash
# Optimizar bash (añadir a ~/.bashrc)
echo 'export HISTSIZE=10000' >> ~/.bashrc
echo 'export HISTFILESIZE=20000' >> ~/.bashrc
echo 'export HISTCONTROL=ignoreboth' >> ~/.bashrc
echo 'shopt -s histappend' >> ~/.bashrc
source ~/.bashrc
```

### Configuración de SSH
```bash
# Optimizar conexiones SSH
cat > ~/.ssh/config << 'EOF'
Host elizaos-vps
    HostName 80.78.30.242
    User markmur88
    IdentityFile ~/.ssh/vps_njalla_nueva
    Port 22
    Compression yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 1h
EOF
```

### Scripts de Automatización
```bash
# Crear script de backup automático
cat > backup_elizaos.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/$USER/elizaos_backups"
mkdir -p $BACKUP_DIR

rsync -avz --exclude='.git' --exclude='node_modules' \
    -e "ssh -i vps_njalla_nueva" \
    markmur88@80.78.30.242:~/elizaos_completo/ \
    $BACKUP_DIR/elizaos_backup_$DATE/

echo "Backup completado: $BACKUP_DIR/elizaos_backup_$DATE"
EOF

chmod +x backup_elizaos.sh
```

## 🐧 Distribuciones Específicas

### Ubuntu/Debian
```bash
# Instalar dependencias específicas
sudo apt update
sudo apt install -y openssh-client rsync curl wget git

# Configurar repositorios si es necesario
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
```

### CentOS/RHEL/Fedora
```bash
# Instalar dependencias específicas
sudo yum install -y openssh-clients rsync curl wget git

# O para Fedora
sudo dnf install -y openssh-clients rsync curl wget git
```

### Arch Linux
```bash
# Instalar dependencias específicas
sudo pacman -S openssh rsync curl wget git

# Configurar AUR si es necesario
yay -S some-package
```

---

## 🎉 ¡ElizaOS en Linux está Listo!

Con esta configuración tienes:
- ✅ Scripts automatizados para Linux
- ✅ Conexión SSH optimizada
- ✅ Monitoreo remoto desde Linux
- ✅ Solución de problemas integrada
- ✅ Documentación específica para Linux
- ✅ Automatización con cron
- ✅ Backup automático

**¡Tu sistema ElizaOS está completamente configurado para Linux y listo para usar!** 