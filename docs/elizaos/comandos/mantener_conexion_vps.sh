#!/bin/bash

# =====================================
# SCRIPT DE CONEXIÓN CONTINUA AL VPS
# =====================================
# Autor: Sistema ElizaOS
# Versión: 1.0
# Descripción: Mantiene conexión SSH continua con reconexión automática

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuración del VPS
VPS_IP="80.78.30.242"
VPS_USER="markmur88"
SSH_KEY="vps_njalla_nueva"
SSH_PORT="22"
PROJECT_DIR="~/elizaos_completo"
LOG_FILE="vps_continuous_connection.log"
MAX_RETRIES=10
RETRY_DELAY=30

# Variables globales
CONNECTION_COUNT=0
LAST_CONNECTION_TIME=""
IS_CONNECTED=false

# Función para logging
log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Función para mostrar banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                CONEXIÓN CONTINUA AL VPS                     ║"
    echo "║                Sistema de Monitoreo                         ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${YELLOW}VPS: $VPS_USER@$VPS_IP${NC}"
    echo -e "${YELLOW}Log: $LOG_FILE${NC}"
    echo ""
}

# Función para verificar conectividad
check_connectivity() {
    if ping -c 1 -W 5 "$VPS_IP" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Función para verificar archivos necesarios
check_requirements() {
    if [ ! -f "$SSH_KEY" ] || [ ! -f "${SSH_KEY}.pub" ]; then
        echo -e "${RED}❌ Faltan archivos SSH necesarios${NC}"
        return 1
    fi
    return 0
}

# Función para establecer conexión SSH
establish_connection() {
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        echo -e "${BLUE}🔄 Intento de conexión $((retry_count + 1))/$MAX_RETRIES${NC}"
        
        if check_connectivity; then
            echo -e "${GREEN}✅ VPS responde al ping${NC}"
            
            # Intentar conexión SSH
            if timeout 30 ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
                -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
                "$VPS_USER@$VPS_IP" "echo 'Conexión SSH exitosa'" > /dev/null 2>&1; then
                
                echo -e "${GREEN}✅ Conexión SSH establecida${NC}"
                CONNECTION_COUNT=$((CONNECTION_COUNT + 1))
                LAST_CONNECTION_TIME=$(date '+%Y-%m-%d %H:%M:%S')
                IS_CONNECTED=true
                log_message "Conexión SSH establecida - Intento $((retry_count + 1))"
                return 0
            else
                echo -e "${YELLOW}⚠️ Conexión SSH falló${NC}"
                log_message "Conexión SSH falló - Intento $((retry_count + 1))"
            fi
        else
            echo -e "${RED}❌ VPS no responde al ping${NC}"
            log_message "VPS no responde al ping - Intento $((retry_count + 1))"
        fi
        
        retry_count=$((retry_count + 1))
        
        if [ $retry_count -lt $MAX_RETRIES ]; then
            echo -e "${YELLOW}⏳ Esperando $RETRY_DELAY segundos antes del siguiente intento...${NC}"
            sleep $RETRY_DELAY
        fi
    done
    
    echo -e "${RED}❌ No se pudo establecer conexión después de $MAX_RETRIES intentos${NC}"
    log_message "Fallo en establecer conexión después de $MAX_RETRIES intentos"
    return 1
}

# Función para mantener conexión SSH interactiva
maintain_interactive_connection() {
    echo -e "${GREEN}🚀 Iniciando conexión SSH interactiva...${NC}"
    echo -e "${CYAN}💡 Usa 'exit' para salir o Ctrl+C para desconectar${NC}"
    echo ""
    
    # Conectar con SSH
    ssh -i "$SSH_KEY" -o ServerAliveInterval=60 -o ServerAliveCountMax=3 \
        -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        "$VPS_USER@$VPS_IP"
}

# Función para mantener conexión SSH con comandos automáticos
maintain_automated_connection() {
    echo -e "${GREEN}🤖 Iniciando conexión SSH automatizada...${NC}"
    
    # Comandos a ejecutar periódicamente
    local commands=(
        "echo '=== Estado del sistema ===' && uptime && free -h && df -h /"
        "echo '=== Servicios ElizaOS ===' && cd $PROJECT_DIR && ls -la 2>/dev/null || echo 'Directorio no encontrado'"
        "echo '=== Conexiones activas ===' && netstat -tlnp 2>/dev/null | grep -E ':(22|80|443|918[0-9]|919[0-9])' || echo 'No hay conexiones activas'"
    )
    
    while true; do
        for cmd in "${commands[@]}"; do
            echo -e "${BLUE}🔧 Ejecutando comando...${NC}"
            
            if ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
                "$VPS_USER@$VPS_IP" "$cmd"; then
                echo -e "${GREEN}✅ Comando ejecutado exitosamente${NC}"
                log_message "Comando ejecutado exitosamente"
            else
                echo -e "${RED}❌ Error ejecutando comando${NC}"
                log_message "Error ejecutando comando"
            fi
            
            echo -e "${YELLOW}⏳ Esperando 60 segundos...${NC}"
            sleep 60
        done
    done
}

# Función para mostrar estadísticas
show_statistics() {
    echo -e "${CYAN}📊 ESTADÍSTICAS DE CONEXIÓN${NC}"
    echo "=================================="
    echo -e "${YELLOW}Conexiones exitosas: $CONNECTION_COUNT${NC}"
    echo -e "${YELLOW}Última conexión: $LAST_CONNECTION_TIME${NC}"
    echo -e "${YELLOW}Estado actual: $([ "$IS_CONNECTED" = true ] && echo "Conectado" || echo "Desconectado")${NC}"
    echo -e "${YELLOW}Archivo de log: $LOG_FILE${NC}"
    echo ""
}

# Función para mostrar menú
show_menu() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                        MENÚ PRINCIPAL                        ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║ 1. 🔌 Conexión interactiva (SSH normal)                     ║"
    echo "║ 2. 🤖 Conexión automatizada (comandos periódicos)           ║"
    echo "║ 3. 🔄 Reconectar automáticamente                            ║"
    echo "║ 4. 📊 Mostrar estadísticas                                  ║"
    echo "║ 5. 🔍 Verificar conectividad                                ║"
    echo "║ 6. 📋 Ver logs                                              ║"
    echo "║ 0. 🚪 Salir                                                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para manejar opciones del menú
handle_menu_option() {
    local option="$1"
    
    case $option in
        1)
            if establish_connection; then
                maintain_interactive_connection
            else
                echo -e "${RED}❌ No se pudo establecer conexión${NC}"
            fi
            ;;
        2)
            if establish_connection; then
                maintain_automated_connection
            else
                echo -e "${RED}❌ No se pudo establecer conexión${NC}"
            fi
            ;;
        3)
            echo -e "${BLUE}🔄 Iniciando reconexión automática...${NC}"
            while true; do
                if ! establish_connection; then
                    echo -e "${YELLOW}⏳ Esperando $RETRY_DELAY segundos antes de reintentar...${NC}"
                    sleep $RETRY_DELAY
                else
                    echo -e "${GREEN}✅ Conexión restablecida${NC}"
                    sleep 10
                fi
            done
            ;;
        4)
            show_statistics
            ;;
        5)
            if check_connectivity; then
                echo -e "${GREEN}✅ VPS responde al ping${NC}"
            else
                echo -e "${RED}❌ VPS no responde al ping${NC}"
            fi
            ;;
        6)
            if [ -f "$LOG_FILE" ]; then
                echo -e "${BLUE}📋 Últimas 20 líneas del log:${NC}"
                tail -20 "$LOG_FILE"
            else
                echo -e "${YELLOW}⚠️ No hay archivo de log${NC}"
            fi
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

# Función para modo automático
auto_mode() {
    echo -e "${GREEN}🤖 Modo automático activado${NC}"
    echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}"
    
    while true; do
        if establish_connection; then
            echo -e "${GREEN}✅ Conexión establecida - ejecutando comandos...${NC}"
            
            # Ejecutar comandos de monitoreo
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
            echo -e "${RED}❌ Conexión fallida - reintentando en $RETRY_DELAY segundos...${NC}"
            sleep $RETRY_DELAY
        fi
    done
}

# Función principal
main() {
    show_banner
    
    # Verificar archivos necesarios
    if ! check_requirements; then
        echo -e "${RED}❌ Faltan archivos necesarios para la conexión${NC}"
        exit 1
    fi
    
    # Verificar argumentos de línea de comandos
    if [ $# -gt 0 ]; then
        case "$1" in
            "interactive"|"interactivo")
                if establish_connection; then
                    maintain_interactive_connection
                fi
                ;;
            "automated"|"automatizado")
                if establish_connection; then
                    maintain_automated_connection
                fi
                ;;
            "auto"|"automatico")
                auto_mode
                ;;
            "reconnect"|"reconectar")
                while true; do
                    if ! establish_connection; then
                        sleep $RETRY_DELAY
                    else
                        sleep 10
                    fi
                done
                ;;
            "status"|"estado")
                show_statistics
                ;;
            "check"|"verificar")
                if check_connectivity; then
                    echo -e "${GREEN}✅ VPS responde al ping${NC}"
                else
                    echo -e "${RED}❌ VPS no responde al ping${NC}"
                fi
                ;;
            "logs")
                if [ -f "$LOG_FILE" ]; then
                    tail -50 "$LOG_FILE"
                else
                    echo -e "${YELLOW}⚠️ No hay archivo de log${NC}"
                fi
                ;;
            *)
                echo -e "${RED}❌ Comando no reconocido: $1${NC}"
                echo -e "${YELLOW}Uso: $0 [interactive|automated|auto|reconnect|status|check|logs]${NC}"
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