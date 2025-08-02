#!/bin/bash

# =====================================
# SCRIPT DE CONEXIÓN CONTINUA AL VPS
# =====================================
# Autor: Sistema ElizaOS
# Versión: 2.0
# Descripción: Script para mantener conexión SSH continua al VPS

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuración del VPS
VPS_IP="80.78.30.242"
VPS_USER="markmur88"
SSH_KEY="vps_njalla_nueva"
SSH_PORT="22"
PROJECT_DIR="~/elizaos_completo"
BACKUP_DIR="~/backups"
LOG_FILE="vps_connection.log"

# Función para mostrar banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    CONEXIÓN VPS ELIZAOS                     ║"
    echo "║                    Sistema de Gestión                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para logging
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Función para verificar conectividad
check_connectivity() {
    echo -e "${BLUE}🔍 Verificando conectividad al VPS...${NC}"
    
    if ping -c 1 -W 5 "$VPS_IP" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ VPS responde al ping${NC}"
        return 0
    else
        echo -e "${RED}❌ VPS no responde al ping${NC}"
        return 1
    fi
}

# Función para verificar archivos necesarios
check_requirements() {
    echo -e "${BLUE}📋 Verificando archivos necesarios...${NC}"
    
    local missing_files=()
    
    if [ ! -f "$SSH_KEY" ]; then
        missing_files+=("$SSH_KEY")
    fi
    
    if [ ! -f "${SSH_KEY}.pub" ]; then
        missing_files+=("${SSH_KEY}.pub")
    fi
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}❌ Archivos faltantes:${NC}"
        for file in "${missing_files[@]}"; do
            echo -e "${RED}   - $file${NC}"
        done
        return 1
    fi
    
    echo -e "${GREEN}✅ Todos los archivos necesarios están presentes${NC}"
    return 0
}

# Función para configurar SSH config
setup_ssh_config() {
    echo -e "${BLUE}⚙️ Configurando SSH config...${NC}"
    
    local ssh_config="$HOME/.ssh/config"
    local config_entry="
Host vps-elizaos
    HostName $VPS_IP
    User $VPS_USER
    IdentityFile $(pwd)/$SSH_KEY
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ConnectTimeout 30
    StrictHostKeyChecking no
"
    
    # Crear directorio .ssh si no existe
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    
    # Verificar si ya existe la configuración
    if grep -q "Host vps-elizaos" "$ssh_config" 2>/dev/null; then
        echo -e "${YELLOW}⚠️ Configuración SSH ya existe${NC}"
    else
        echo "$config_entry" >> "$ssh_config"
        chmod 600 "$ssh_config"
        echo -e "${GREEN}✅ Configuración SSH agregada${NC}"
    fi
}

# Función para conectar al VPS
connect_vps() {
    echo -e "${BLUE}🔌 Conectando al VPS...${NC}"
    
    # Verificar conectividad
    if ! check_connectivity; then
        echo -e "${RED}❌ No se puede conectar al VPS${NC}"
        return 1
    fi
    
    # Verificar archivos
    if ! check_requirements; then
        echo -e "${RED}❌ Faltan archivos necesarios${NC}"
        return 1
    fi
    
    # Configurar SSH
    setup_ssh_config
    
    log_message "Iniciando conexión SSH al VPS"
    
    echo -e "${GREEN}🚀 Conectando a $VPS_USER@$VPS_IP...${NC}"
    echo -e "${CYAN}💡 Usa 'exit' para salir o Ctrl+C para desconectar${NC}"
    echo ""
    
    # Conectar con SSH
    ssh -i "$SSH_KEY" -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
        -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        "$VPS_USER@$VPS_IP"
}

# Función para conectar y ejecutar comando específico
execute_command() {
    local command="$1"
    echo -e "${BLUE}🔧 Ejecutando comando: $command${NC}"
    
    ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        "$VPS_USER@$VPS_IP" "$command"
}

# Función para subir archivos
upload_files() {
    local source="$1"
    local destination="$2"
    
    if [ -z "$destination" ]; then
        destination="$PROJECT_DIR"
    fi
    
    echo -e "${BLUE}📤 Subiendo archivos...${NC}"
    echo -e "${CYAN}Origen: $source${NC}"
    echo -e "${CYAN}Destino: $destination${NC}"
    
    scp -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        -r "$source" "$VPS_USER@$VPS_IP:$destination"
    
    echo -e "${GREEN}✅ Archivos subidos correctamente${NC}"
}

# Función para descargar archivos
download_files() {
    local source="$1"
    local destination="$2"
    
    if [ -z "$destination" ]; then
        destination="."
    fi
    
    echo -e "${BLUE}📥 Descargando archivos...${NC}"
    echo -e "${CYAN}Origen: $source${NC}"
    echo -e "${CYAN}Destino: $destination${NC}"
    
    scp -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        -r "$VPS_USER@$VPS_IP:$source" "$destination"
    
    echo -e "${GREEN}✅ Archivos descargados correctamente${NC}"
}

# Función para mostrar estado del VPS
show_status() {
    echo -e "${BLUE}📊 Estado del VPS...${NC}"
    
    execute_command "
        echo '=== INFORMACIÓN DEL SISTEMA ==='
        echo 'Hostname:' \$(hostname)
        echo 'Uptime:' \$(uptime -p)
        echo 'Carga del sistema:' \$(uptime | awk -F'load average:' '{print \$2}')
        echo 'Memoria:' \$(free -h | grep '^Mem' | awk '{print \$3"/"\$2}')
        echo 'Disco:' \$(df -h / | tail -1 | awk '{print \$3"/"\$2}')
        echo 'Procesos activos:' \$(ps aux | wc -l)
        echo ''
        echo '=== SERVICIOS ELIZAOS ==='
        if [ -d '$PROJECT_DIR' ]; then
            echo '✅ Directorio ElizaOS encontrado'
            cd $PROJECT_DIR
            echo 'Puertos en uso:'
            netstat -tlnp 2>/dev/null | grep -E ':(918[0-9]|919[0-9])' || echo 'No hay puertos ElizaOS activos'
        else
            echo '❌ Directorio ElizaOS no encontrado'
        fi
        echo ''
        echo '=== CONEXIONES ACTIVAS ==='
        netstat -tlnp 2>/dev/null | grep -E ':(22|80|443|918[0-9]|919[0-9])' || echo 'No hay conexiones activas'
    "
}

# Función para reiniciar servicios
restart_services() {
    echo -e "${BLUE}🔄 Reiniciando servicios ElizaOS...${NC}"
    
    execute_command "
        if [ -d '$PROJECT_DIR' ]; then
            cd $PROJECT_DIR
            echo 'Deteniendo servicios...'
            pkill -f 'elizaos' || true
            pkill -f 'agente' || true
            sleep 2
            echo 'Iniciando servicios...'
            if [ -f 'scripts/levantar_sistema_completo.sh' ]; then
                chmod +x scripts/levantar_sistema_completo.sh
                ./scripts/levantar_sistema_completo.sh
            elif [ -f 'agentes_elizaos/scripts/levantar_sistema_completo.sh' ]; then
                chmod +x agentes_elizaos/scripts/levantar_sistema_completo.sh
                ./agentes_elizaos/scripts/levantar_sistema_completo.sh
            else
                echo '❌ No se encontraron scripts de inicio'
            fi
        else
            echo '❌ Directorio ElizaOS no encontrado'
        fi
    "
}

# Función para hacer backup
create_backup() {
    local backup_name="elizaos_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    
    echo -e "${BLUE}💾 Creando backup...${NC}"
    
    execute_command "
        if [ -d '$PROJECT_DIR' ]; then
            mkdir -p $BACKUP_DIR
            cd $PROJECT_DIR/..
            tar -czf $BACKUP_DIR/$backup_name elizaos_completo/
            echo '✅ Backup creado: $backup_name'
            echo 'Tamaño:' \$(du -h $BACKUP_DIR/$backup_name | cut -f1)
        else
            echo '❌ Directorio ElizaOS no encontrado'
        fi
    "
}

# Función para mostrar logs
show_logs() {
    echo -e "${BLUE}📋 Mostrando logs recientes...${NC}"
    
    execute_command "
        echo '=== LOGS DEL SISTEMA ==='
        journalctl --since '1 hour ago' | grep -i elizaos | tail -20
        echo ''
        echo '=== LOGS DE SERVICIOS ==='
        if [ -d '$PROJECT_DIR' ]; then
            find $PROJECT_DIR -name '*.log' -exec tail -10 {} \; 2>/dev/null || echo 'No se encontraron logs'
        fi
    "
}

# Función para mostrar menú principal
show_menu() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                        MENÚ PRINCIPAL                        ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║ 1. 🔌 Conectar al VPS (SSH interactivo)                     ║"
    echo "║ 2. 📊 Mostrar estado del VPS                                ║"
    echo "║ 3. 🔄 Reiniciar servicios ElizaOS                          ║"
    echo "║ 4. 💾 Crear backup                                          ║"
    echo "║ 5. 📋 Mostrar logs                                          ║"
    echo "║ 6. 📤 Subir archivos                                        ║"
    echo "║ 7. 📥 Descargar archivos                                    ║"
    echo "║ 8. ⚙️ Configurar SSH                                        ║"
    echo "║ 9. 🔍 Verificar conectividad                                ║"
    echo "║ 0. 🚪 Salir                                                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para manejar opciones del menú
handle_menu_option() {
    local option="$1"
    
    case $option in
        1)
            connect_vps
            ;;
        2)
            show_status
            ;;
        3)
            restart_services
            ;;
        4)
            create_backup
            ;;
        5)
            show_logs
            ;;
        6)
            echo -e "${YELLOW}📤 Ingresa la ruta del archivo/carpeta a subir:${NC}"
            read -r source_path
            if [ -n "$source_path" ] && [ -e "$source_path" ]; then
                upload_files "$source_path"
            else
                echo -e "${RED}❌ Ruta inválida o archivo no existe${NC}"
            fi
            ;;
        7)
            echo -e "${YELLOW}📥 Ingresa la ruta del archivo/carpeta a descargar:${NC}"
            read -r source_path
            if [ -n "$source_path" ]; then
                download_files "$source_path"
            else
                echo -e "${RED}❌ Ruta inválida${NC}"
            fi
            ;;
        8)
            setup_ssh_config
            ;;
        9)
            check_connectivity
            ;;
        0)
            echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida${NC}"
            ;;
    esac
}

# Función principal
main() {
    show_banner
    
    # Verificar argumentos de línea de comandos
    if [ $# -gt 0 ]; then
        case "$1" in
            "connect"|"conectar")
                connect_vps
                ;;
            "status"|"estado")
                show_status
                ;;
            "restart"|"reiniciar")
                restart_services
                ;;
            "backup")
                create_backup
                ;;
            "logs")
                show_logs
                ;;
            "upload"|"subir")
                if [ -n "$2" ]; then
                    upload_files "$2"
                else
                    echo -e "${RED}❌ Debes especificar la ruta del archivo${NC}"
                    exit 1
                fi
                ;;
            "download"|"descargar")
                if [ -n "$2" ]; then
                    download_files "$2"
                else
                    echo -e "${RED}❌ Debes especificar la ruta del archivo${NC}"
                    exit 1
                fi
                ;;
            "setup"|"configurar")
                setup_ssh_config
                ;;
            "check"|"verificar")
                check_connectivity
                ;;
            *)
                echo -e "${RED}❌ Comando no reconocido: $1${NC}"
                echo -e "${YELLOW}Uso: $0 [connect|status|restart|backup|logs|upload|download|setup|check]${NC}"
                exit 1
                ;;
        esac
    else
        # Modo interactivo
        while true; do
            show_menu
            echo -e "${YELLOW}Selecciona una opción:${NC}"
            read -r option
            echo ""
            handle_menu_option "$option"
            echo ""
            echo -e "${CYAN}Presiona Enter para continuar...${NC}"
            read -r
        done
    fi
}

# Manejo de señales
trap 'echo -e "\n${YELLOW}⚠️ Conexión interrumpida${NC}"; exit 1' INT TERM

# Ejecutar función principal
main "$@" 