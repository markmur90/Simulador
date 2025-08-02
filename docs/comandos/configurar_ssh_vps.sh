#!/bin/bash

# =====================================
# CONFIGURACIÓN AUTOMÁTICA SSH VPS
# =====================================
# Autor: Sistema ElizaOS
# Versión: 1.0
# Descripción: Configura automáticamente el entorno SSH para el VPS

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
SSH_CONFIG="$HOME/.ssh/config"

# Función para mostrar banner
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                CONFIGURACIÓN SSH VPS                        ║"
    echo "║                Sistema ElizaOS                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "${YELLOW}VPS: $VPS_USER@$VPS_IP${NC}"
    echo -e "${YELLOW}Clave SSH: $SSH_KEY${NC}"
    echo ""
}

# Función para verificar archivos SSH
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

# Función para configurar permisos SSH
setup_ssh_permissions() {
    echo -e "${BLUE}🔐 Configurando permisos SSH...${NC}"
    
    # Configurar permisos de la clave privada
    if [ -f "$SSH_KEY" ]; then
        chmod 600 "$SSH_KEY"
        echo -e "${GREEN}✅ Permisos de clave privada configurados${NC}"
    fi
    
    # Configurar permisos de la clave pública
    if [ -f "${SSH_KEY}.pub" ]; then
        chmod 644 "${SSH_KEY}.pub"
        echo -e "${GREEN}✅ Permisos de clave pública configurados${NC}"
    fi
    
    # Crear y configurar directorio .ssh
    mkdir -p "$HOME/.ssh"
    chmod 700 "$HOME/.ssh"
    echo -e "${GREEN}✅ Directorio .ssh configurado${NC}"
}

# Función para configurar SSH config
setup_ssh_config() {
    echo -e "${BLUE}⚙️ Configurando SSH config...${NC}"
    
    # Crear backup del config existente
    if [ -f "$SSH_CONFIG" ]; then
        cp "$SSH_CONFIG" "${SSH_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}⚠️ Backup del SSH config creado${NC}"
    fi
    
    # Configuración para el VPS
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

# Configuración alternativa con IP directa
Host $VPS_IP
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
    
    # Agregar configuración al SSH config
    echo "$config_entry" >> "$SSH_CONFIG"
    chmod 600 "$SSH_CONFIG"
    
    echo -e "${GREEN}✅ SSH config configurado${NC}"
    echo -e "${CYAN}💡 Ahora puedes usar: ssh vps-elizaos${NC}"
}

# Función para verificar conectividad SSH
test_ssh_connection() {
    echo -e "${BLUE}🧪 Probando conexión SSH...${NC}"
    
    # Probar con nombre de host
    echo -e "${YELLOW}Probando conexión con 'vps-elizaos'...${NC}"
    if timeout 30 ssh -o ConnectTimeout=30 vps-elizaos "echo 'Conexión SSH exitosa'" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Conexión SSH exitosa con 'vps-elizaos'${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️ Conexión con 'vps-elizaos' falló${NC}"
    fi
    
    # Probar con IP directa
    echo -e "${YELLOW}Probando conexión con IP directa...${NC}"
    if timeout 30 ssh -i "$SSH_KEY" -o ConnectTimeout=30 -o StrictHostKeyChecking=no \
        "$VPS_USER@$VPS_IP" "echo 'Conexión SSH exitosa'" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Conexión SSH exitosa con IP directa${NC}"
        return 0
    else
        echo -e "${RED}❌ Conexión SSH falló${NC}"
        return 1
    fi
}

# Función para configurar alias útiles
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
    
    # Verificar si los alias ya existen
    if grep -q "alias vps=" "$bashrc" 2>/dev/null; then
        echo -e "${YELLOW}⚠️ Alias ya existen en .bashrc${NC}"
    else
        echo "$aliases" >> "$bashrc"
        echo -e "${GREEN}✅ Alias agregados a .bashrc${NC}"
        echo -e "${CYAN}💡 Recarga tu terminal o ejecuta: source ~/.bashrc${NC}"
    fi
}

# Función para crear script de conexión rápida
create_quick_connect_script() {
    echo -e "${BLUE}🚀 Creando script de conexión rápida...${NC}"
    
    local quick_script="quick_vps.sh"
    
    cat > "$quick_script" << 'EOF'
#!/bin/bash

# Script de conexión rápida al VPS
echo "🚀 Conectando al VPS ElizaOS..."

# Verificar conectividad
if ping -c 1 -W 5 80.78.30.242 > /dev/null 2>&1; then
    echo "✅ VPS responde al ping"
    
    # Intentar conexión SSH
    if ssh -o ConnectTimeout=30 vps-elizaos "echo 'Conexión exitosa'" > /dev/null 2>&1; then
        echo "✅ Conexión SSH disponible"
        echo "🔌 Conectando..."
        ssh vps-elizaos
    else
        echo "❌ Error en conexión SSH"
        echo "🔧 Intentando con IP directa..."
        ssh -i vps_njalla_nueva -o ConnectTimeout=30 -o StrictHostKeyChecking=no markmur88@80.78.30.242
    fi
else
    echo "❌ VPS no responde al ping"
    echo "🔍 Verificando conectividad de red..."
    ping -c 3 8.8.8.8
fi
EOF
    
    chmod +x "$quick_script"
    echo -e "${GREEN}✅ Script de conexión rápida creado: $quick_script${NC}"
}

# Función para mostrar información de configuración
show_config_info() {
    echo -e "${CYAN}📊 INFORMACIÓN DE CONFIGURACIÓN${NC}"
    echo "=================================="
    echo -e "${YELLOW}VPS IP: $VPS_IP${NC}"
    echo -e "${YELLOW}Usuario: $VPS_USER${NC}"
    echo -e "${YELLOW}Clave SSH: $SSH_KEY${NC}"
    echo -e "${YELLOW}SSH Config: $SSH_CONFIG${NC}"
    echo ""
    echo -e "${GREEN}🚀 Comandos disponibles:${NC}"
    echo -e "${CYAN}  ssh vps-elizaos${NC} - Conectar al VPS"
    echo -e "${CYAN}  vps${NC} - Alias para conectar (después de recargar .bashrc)"
    echo -e "${CYAN}  vps-status${NC} - Ver estado del VPS"
    echo -e "${CYAN}  vps-logs${NC} - Ver logs de ElizaOS"
    echo -e "${CYAN}  vps-restart${NC} - Reiniciar servicios"
    echo -e "${CYAN}  vps-backup${NC} - Crear backup"
    echo -e "${CYAN}  vps-monitor${NC} - Monitorear procesos"
    echo -e "${CYAN}  ./quick_vps.sh${NC} - Conexión rápida"
    echo ""
}

# Función para mostrar menú
show_menu() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                        MENÚ PRINCIPAL                        ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║ 1. 🔧 Configuración completa automática                     ║"
    echo "║ 2. 🔐 Configurar permisos SSH                              ║"
    echo "║ 3. ⚙️ Configurar SSH config                                ║"
    echo "║ 4. 📝 Configurar alias                                     ║"
    echo "║ 5. 🚀 Crear script de conexión rápida                      ║"
    echo "║ 6. 🧪 Probar conexión SSH                                  ║"
    echo "║ 7. 📊 Mostrar información de configuración                 ║"
    echo "║ 8. 🔍 Verificar archivos SSH                               ║"
    echo "║ 0. 🚪 Salir                                                 ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Función para manejar opciones del menú
handle_menu_option() {
    local option="$1"
    
    case $option in
        1)
            echo -e "${BLUE}🔧 Configuración completa automática...${NC}"
            if check_ssh_files; then
                setup_ssh_permissions
                setup_ssh_config
                setup_aliases
                create_quick_connect_script
                test_ssh_connection
                show_config_info
            fi
            ;;
        2)
            setup_ssh_permissions
            ;;
        3)
            setup_ssh_config
            ;;
        4)
            setup_aliases
            ;;
        5)
            create_quick_connect_script
            ;;
        6)
            test_ssh_connection
            ;;
        7)
            show_config_info
            ;;
        8)
            check_ssh_files
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
            "auto"|"automatico")
                echo -e "${BLUE}🔧 Configuración automática...${NC}"
                if check_ssh_files; then
                    setup_ssh_permissions
                    setup_ssh_config
                    setup_aliases
                    create_quick_connect_script
                    test_ssh_connection
                    show_config_info
                fi
                ;;
            "test"|"probar")
                test_ssh_connection
                ;;
            "info"|"informacion")
                show_config_info
                ;;
            "check"|"verificar")
                check_ssh_files
                ;;
            *)
                echo -e "${RED}❌ Comando no reconocido: $1${NC}"
                echo -e "${YELLOW}Uso: $0 [auto|test|info|check]${NC}"
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

# Ejecutar función principal
main "$@" 