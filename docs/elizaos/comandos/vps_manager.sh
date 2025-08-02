#!/bin/bash

# =====================================
# GESTOR COMPLETO DE VPS ELIZAOS
# =====================================
# Autor: Sistema ElizaOS
# Versión: 3.0
# Descripción: Gestor completo para administrar el VPS de ElizaOS

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
LOG_FILE="vps_manager.log"
SSH_CONFIG="$HOME/.ssh/config"

# Variables globales
CONNECTION_COUNT=0
LAST_CONNECTION_TIME=""
IS_CONNECTED=false

# Función para mostrar banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                GESTOR COMPLETO DE VPS ELIZAOS                ║"
    echo "║                    Sistema de Administración                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${YELLOW}VPS: $VPS_USER@$VPS_IP${NC}"
    echo -e "${YELLOW}Proyecto: $PROJECT_DIR${NC}"
    echo -e "${YELLOW}Log: $LOG_FILE${NC}"
    echo ""
}

# Función para logging
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# =====================================
# FUNCIONES DE CONFIGURACIÓN SSH
# =====================================

# Verificar archivos SSH
check_ssh_files() {
    echo -e "${BLUE}📋 Verificando archivos SSH...${NC}"
    
    local missing_files=()
    
    if [ ! -f "$SSH_KEY" ]; then
        missing_files+=("$SSH_KEY")
    fi
    
    if [ ! -f "${SSH_KEY}.pub" ]; then
        missing_files+=("${SSH_KEY}.pub")
    fi
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}❌ Archivos SSH faltantes:${NC}"
        for file in "${missing_files[@]}"; do
            echo -e "${RED}   - $file${NC}"
        done
        return 1
    fi
    
    echo -e "${GREEN}✅ Archivos SSH encontrados${NC}"
    return 0
}

# Configurar permisos SSH
setup_ssh_permissions() {
    echo -e "${BLUE}🔐 Configurando permisos SSH...${NC}"
    
    if [ -f "$SSH_KEY" ]; then
        chmod 600 "$SSH_KEY"
        echo -e "${GREEN}✅ Permisos de clave privada configurados${NC}"
    fi
    
    if [ -f "${SSH_KEY}.pub" ]; then
        chmod 644 "${SSH_KEY}.pub"
        echo -e "${GREEN}✅ Permisos de clave pública configurados${NC}"
    fi
    
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    echo -e "${GREEN}✅ Directorio .ssh configurado${NC}"
}

# Configurar SSH config
setup_ssh_config() {
    echo -e "${BLUE}⚙️ Configurando SSH config...${NC}"
    
    if [ -f "$SSH_CONFIG" ]; then
        cp "$SSH_CONFIG" "${SSH_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}⚠️ Backup del SSH config creado${NC}"
    fi
    
    local config_entry="
# Configuración para VPS ElizaOS
Host vps-elizaos
    HostName $VPS_IP
    User $VPS_USER
    IdentityFile $(pwd)/$SSH_KEY
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ConnectTimeout 30
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
"
    
    echo "$config_entry" >> "$SSH_CONFIG"
    chmod 600 "$SSH_CONFIG"
    
    echo -e "${GREEN}✅ SSH config configurado${NC}"
    echo -e "${CYAN}💡 Ahora puedes usar: ssh vps-elizaos${NC}"
}

# =====================================
# FUNCIONES DE CONECTIVIDAD
# =====================================

# Verificar conectividad
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

# Establecer conexión SSH
establish_connection() {
    local retry_count=0
    local max_retries=5
    
    while [ $retry_count -lt $max_retries ]; do
        echo -e "${BLUE}🔄 Intento de conexión $((retry_count + 1))/$max_retries${NC}"
        
        if check_connectivity; then
            if timeout 30 ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
                -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
                "$VPS_USER@$VPS_IP" "echo 'Conexión SSH exitosa'" > /dev/null 2>&1; then
                
                echo -e "${GREEN}✅ Conexión SSH establecida${NC}"
                CONNECTION_COUNT=$((CONNECTION_COUNT + 1))
                LAST_CONNECTION_TIME=$(date '+%Y-%m-%d %H:%M:%S')
                IS_CONNECTED=true
                log_message "Conexión SSH establecida"
                return 0
            else
                echo -e "${YELLOW}⚠️ Conexión SSH falló${NC}"
            fi
        fi
        
        retry_count=$((retry_count + 1))
        if [ $retry_count -lt $max_retries ]; then
            echo -e "${YELLOW}⏳ Esperando 10 segundos...${NC}"
            sleep 10
        fi
    done
    
    echo -e "${RED}❌ No se pudo establecer conexión${NC}"
    return 1
}

# =====================================
# FUNCIONES DE CONEXIÓN
# =====================================

# Conexión SSH interactiva
connect_interactive() {
    echo -e "${BLUE}🔌 Conectando al VPS...${NC}"
    
    if ! check_requirements; then
        echo -e "${RED}❌ Faltan archivos necesarios${NC}"
        return 1
    fi
    
    if ! establish_connection; then
        echo -e "${RED}❌ No se puede conectar al VPS${NC}"
        return 1
    fi
    
    log_message "Iniciando conexión SSH interactiva"
    
    echo -e "${GREEN}🚀 Conectando a $VPS_USER@$VPS_IP...${NC}"
    echo -e "${CYAN}💡 Usa 'exit' para salir o Ctrl+C para desconectar${NC}"
    echo ""
    
    ssh -i "$SSH_KEY" -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
        -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        "$VPS_USER@$VPS_IP"
}

# Conexión SSH con reconexión automática
connect_continuous() {
    echo -e "${BLUE}🔄 Iniciando conexión continua...${NC}"
    echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}"
    
    while true; do
        if establish_connection; then
            echo -e "${GREEN}✅ Conexión establecida - ejecutando comandos...${NC}"
            
            ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
                "$VPS_USER@$VPS_IP" "
                    echo '=== $(date) ==='
                    echo 'Uptime:' \$(uptime -p)
                    echo 'Memoria:' \$(free -h | grep '^Mem' | awk '{print \$3"/"\$2}')
                    echo 'Disco:' \$(df -h / | tail -1 | awk '{print \$3"/"\$2}')
                    echo 'Procesos ElizaOS:' \$(ps aux | grep -i elizaos | wc -l)
                    echo '---'
                " 2>/dev/null || echo "Error ejecutando comandos"
            
            sleep 300  # Esperar 5 minutos
        else
            echo -e "${RED}❌ Conexión fallida - reintentando en 30 segundos...${NC}"
            sleep 30
        fi
    done
}

# =====================================
# FUNCIONES DE GESTIÓN
# =====================================

# Ejecutar comando en el VPS
execute_command() {
    local command="$1"
    echo -e "${BLUE}🔧 Ejecutando comando: $command${NC}"
    
    ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        "$VPS_USER@$VPS_IP" "$command"
}

# Mostrar estado del VPS
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

# Reiniciar servicios
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

# Crear backup
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

# Mostrar logs
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

# =====================================
# FUNCIONES DE TRANSFERENCIA
# =====================================

# Subir archivos
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

# Descargar archivos
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

# =====================================
# FUNCIONES DE CONFIGURACIÓN
# =====================================

# Configurar alias
setup_aliases() {
    echo -e "${BLUE}📝 Configurando alias útiles...${NC}"
    
    local bashrc="$HOME/.bashrc"
    local aliases="
# Alias para VPS ElizaOS
alias vps='ssh vps-elizaos'
alias vps-status='ssh vps-elizaos \"uptime && free -h && df -h /\"'
alias vps-logs='ssh vps-elizaos \"cd ~/elizaos_completo && find . -name \\\"*.log\\\" -exec tail -10 {} \\;\"'
alias vps-restart='ssh vps-elizaos \"cd ~/elizaos_completo && ./scripts/levantar_sistema_completo.sh\"'
alias vps-backup='ssh vps-elizaos \"cd ~ && tar -czf backup_elizaos_\$(date +%Y%m%d_%H%M%S).tar.gz elizaos_completo/\"'
alias vps-monitor='ssh vps-elizaos \"watch -n 5 \\\"ps aux | grep elizaos && echo \\\"---\\\" && netstat -tlnp | grep :918\"\"'
"
    
    if grep -q "alias vps=" "$bashrc" 2>/dev/null; then
        echo -e "${YELLOW}⚠️ Alias ya existen en .bashrc${NC}"
    else
        echo "$aliases" >> "$bashrc"
        echo -e "${GREEN}✅ Alias agregados a .bashrc${NC}"
        echo -e "${CYAN}💡 Recarga tu terminal o ejecuta: source ~/.bashrc${NC}"
    fi
}

# Configuración completa
setup_complete() {
    echo -e "${BLUE}🔧 Configuración completa automática...${NC}"
    
    if check_ssh_files; then
        setup_ssh_permissions
        setup_ssh_config
        setup_aliases
        establish_connection
        show_config_info
    fi
}

# =====================================
# FUNCIONES DE INFORMACIÓN
# =====================================

# Mostrar información de configuración
show_config_info() {
    echo -e "${CYAN}📊 INFORMACIÓN DE CONFIGURACIÓN${NC}"
    echo "=================================="
    echo -e "${YELLOW}VPS IP: $VPS_IP${NC}"
    echo -e "${YELLOW}Usuario: $VPS_USER${NC}"
    echo -e "${YELLOW}Clave SSH: $SSH_KEY${NC}"
    echo -e "${YELLOW}SSH Config: $SSH_CONFIG${NC}"
    echo -e "${YELLOW}Conexiones exitosas: $CONNECTION_COUNT${NC}"
    echo -e "${YELLOW}Última conexión: $LAST_CONNECTION_TIME${NC}"
    echo ""
    echo -e "${GREEN}🚀 Comandos disponibles:${NC}"
    echo -e "${CYAN}  ssh vps-elizaos${NC} - Conectar al VPS"
    echo -e "${CYAN}  vps${NC} - Alias para conectar"
    echo -e "${CYAN}  vps-status${NC} - Ver estado del VPS"
    echo -e "${CYAN}  vps-logs${NC} - Ver logs de ElizaOS"
    echo -e "${CYAN}  vps-restart${NC} - Reiniciar servicios"
    echo -e "${CYAN}  vps-backup${NC} - Crear backup"
    echo -e "${CYAN}  vps-monitor${NC} - Monitorear procesos"
    echo ""
}

# Verificar requisitos
check_requirements() {
    if ! check_ssh_files; then
        return 1
    fi
    return 0
}

# =====================================
# MENÚ PRINCIPAL
# =====================================

# Mostrar menú principal
show_menu() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                        MENÚ PRINCIPAL                        ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║ 🔌 CONEXIÓN:                                                ║"
    echo "║   1. Conectar al VPS (SSH interactivo)                      ║"
    echo "║   2. Conexión continua (monitoreo automático)               ║"
    echo "║   3. Verificar conectividad                                 ║"
    echo "║                                                              ║"
    echo "║ 📊 GESTIÓN:                                                 ║"
    echo "║   4. Mostrar estado del VPS                                 ║"
    echo "║   5. Reiniciar servicios ElizaOS                            ║"
    echo "║   6. Crear backup                                           ║"
    echo "║   7. Mostrar logs                                           ║"
    echo "║                                                              ║"
    echo "║ 📁 TRANSFERENCIA:                                           ║"
    echo "║   8. Subir archivos                                         ║"
    echo "║   9. Descargar archivos                                     ║"
    echo "║                                                              ║"
    echo "║ ⚙️ CONFIGURACIÓN:                                           ║"
    echo "║   10. Configuración completa automática                     ║"
    echo "║   11. Configurar SSH                                        ║"
    echo "║   12. Configurar alias                                      ║"
    echo "║   13. Mostrar información de configuración                  ║"
    echo "║                                                              ║"
    echo "║ 0. 🚪 Salir                                                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Manejar opciones del menú
handle_menu_option() {
    local option="$1"
    
    case $option in
        1)
            connect_interactive
            ;;
        2)
            connect_continuous
            ;;
        3)
            check_connectivity
            ;;
        4)
            show_status
            ;;
        5)
            restart_services
            ;;
        6)
            create_backup
            ;;
        7)
            show_logs
            ;;
        8)
            echo -e "${YELLOW}📤 Ingresa la ruta del archivo/carpeta a subir:${NC}"
            read -r source_path
            if [ -n "$source_path" ] && [ -e "$source_path" ]; then
                upload_files "$source_path"
            else
                echo -e "${RED}❌ Ruta inválida o archivo no existe${NC}"
            fi
            ;;
        9)
            echo -e "${YELLOW}📥 Ingresa la ruta del archivo/carpeta a descargar:${NC}"
            read -r source_path
            if [ -n "$source_path" ]; then
                download_files "$source_path"
            else
                echo -e "${RED}❌ Ruta inválida${NC}"
            fi
            ;;
        10)
            setup_complete
            ;;
        11)
            if check_ssh_files; then
                setup_ssh_permissions
                setup_ssh_config
            fi
            ;;
        12)
            setup_aliases
            ;;
        13)
            show_config_info
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

# =====================================
# FUNCIÓN PRINCIPAL
# =====================================

main() {
    show_banner
    
    # Verificar argumentos de línea de comandos
    if [ $# -gt 0 ]; then
        case "$1" in
            "connect"|"conectar")
                connect_interactive
                ;;
            "continuous"|"continuo")
                connect_continuous
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
                setup_complete
                ;;
            "check"|"verificar")
                check_connectivity
                ;;
            "info"|"informacion")
                show_config_info
                ;;
            *)
                echo -e "${RED}❌ Comando no reconocido: $1${NC}"
                echo -e "${YELLOW}Uso: $0 [connect|continuous|status|restart|backup|logs|upload|download|setup|check|info]${NC}"
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
trap 'echo -e "\n${YELLOW}⚠️ Conexión interrumpida${NC}"; log_message "Conexión interrumpida por el usuario"; exit 1' INT TERM

# Ejecutar función principal
main "$@" 