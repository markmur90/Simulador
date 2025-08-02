# 🚀 Gestión Completa de VPS ElizaOS

Este conjunto de scripts proporciona una solución completa para gestionar el VPS de ElizaOS de forma eficiente y segura.

## 📋 Scripts Disponibles

### 1. `vps_manager.sh` - Gestor Principal
Script maestro que combina todas las funcionalidades en una sola herramienta.

### 2. `conectar_vps.sh` - Conexión Básica
Script para conexiones SSH simples y gestión básica del VPS.

### 3. `mantener_conexion_vps.sh` - Conexión Continua
Script para mantener conexiones SSH continuas con reconexión automática.

### 4. `configurar_ssh_vps.sh` - Configuración SSH
Script para configurar automáticamente el entorno SSH.

## 🚀 Instalación y Configuración

### Requisitos Previos
- Archivos SSH: `vps_njalla_nueva` y `vps_njalla_nueva.pub`
- Acceso al VPS: `markmur88@80.78.30.242`
- Bash shell

### Configuración Inicial
```bash
# Dar permisos de ejecución a todos los scripts
chmod +x *.sh

# Configuración automática completa
./vps_manager.sh setup
```

## 📖 Uso de los Scripts

### Gestor Principal (`vps_manager.sh`)

#### Modo Interactivo
```bash
./vps_manager.sh
```

#### Modo de Comandos
```bash
# Conectar al VPS
./vps_manager.sh connect

# Conexión continua con monitoreo
./vps_manager.sh continuous

# Ver estado del VPS
./vps_manager.sh status

# Reiniciar servicios
./vps_manager.sh restart

# Crear backup
./vps_manager.sh backup

# Ver logs
./vps_manager.sh logs

# Subir archivos
./vps_manager.sh upload /ruta/archivo

# Descargar archivos
./vps_manager.sh download /ruta/archivo

# Verificar conectividad
./vps_manager.sh check

# Mostrar información
./vps_manager.sh info
```

### Conexión Básica (`conectar_vps.sh`)

```bash
# Modo interactivo
./conectar_vps.sh

# Comandos específicos
./conectar_vps.sh connect      # Conectar SSH
./conectar_vps.sh status       # Estado del VPS
./conectar_vps.sh restart      # Reiniciar servicios
./conectar_vps.sh backup       # Crear backup
./conectar_vps.sh logs         # Ver logs
./conectar_vps.sh upload archivo  # Subir archivo
./conectar_vps.sh download archivo # Descargar archivo
```

### Conexión Continua (`mantener_conexion_vps.sh`)

```bash
# Modo interactivo
./mantener_conexion_vps.sh

# Conexión interactiva
./mantener_conexion_vps.sh interactive

# Conexión automatizada
./mantener_conexion_vps.sh automated

# Reconexión automática
./mantener_conexion_vps.sh reconnect

# Modo automático
./mantener_conexion_vps.sh auto
```

### Configuración SSH (`configurar_ssh_vps.sh`)

```bash
# Configuración automática completa
./configurar_ssh_vps.sh auto

# Probar conexión SSH
./configurar_ssh_vps.sh test

# Ver información de configuración
./configurar_ssh_vps.sh info

# Verificar archivos SSH
./configurar_ssh_vps.sh check
```

## 🔧 Funcionalidades Principales

### 🔌 Conexión SSH
- **Conexión interactiva**: SSH normal con acceso completo al VPS
- **Conexión continua**: Monitoreo automático con reconexión
- **Verificación de conectividad**: Ping y pruebas de conexión SSH
- **Configuración automática**: SSH config y alias

### 📊 Gestión del Sistema
- **Estado del VPS**: Uptime, memoria, disco, procesos
- **Servicios ElizaOS**: Monitoreo de puertos y procesos
- **Reinicio de servicios**: Detener e iniciar servicios automáticamente
- **Backups**: Creación automática de respaldos

### 📁 Transferencia de Archivos
- **Subir archivos**: SCP automático al VPS
- **Descargar archivos**: SCP desde el VPS
- **Verificación**: Comprobación de archivos antes de transferir

### 📋 Logs y Monitoreo
- **Logs del sistema**: journalctl y logs de servicios
- **Logs de ElizaOS**: Archivos de log específicos del proyecto
- **Monitoreo en tiempo real**: Estado continuo del sistema

## 🛠️ Configuración SSH Automática

### Alias Configurados
Después de ejecutar la configuración, tendrás estos alias disponibles:

```bash
vps              # Conectar al VPS
vps-status       # Ver estado del VPS
vps-logs         # Ver logs de ElizaOS
vps-restart      # Reiniciar servicios
vps-backup       # Crear backup
vps-monitor      # Monitorear procesos
```

### SSH Config
Se crea automáticamente en `~/.ssh/config`:

```
Host vps-elizaos
    HostName 80.78.30.242
    User markmur88
    IdentityFile /ruta/vps_njalla_nueva
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ConnectTimeout 30
    StrictHostKeyChecking no
```

## 📊 Monitoreo y Logs

### Archivos de Log
- `vps_connection.log`: Logs de conexiones SSH
- `vps_continuous_connection.log`: Logs de conexión continua
- `vps_manager.log`: Logs del gestor principal

### Información Monitoreada
- **Sistema**: Uptime, carga, memoria, disco
- **Servicios**: Procesos ElizaOS, puertos activos
- **Conexiones**: Estado de conexiones SSH y servicios
- **Errores**: Fallos de conexión y problemas del sistema

## 🔒 Seguridad

### Características de Seguridad
- **Permisos SSH**: Configuración automática de permisos (600/700)
- **Claves SSH**: Uso exclusivo de claves SSH (sin contraseñas)
- **Timeouts**: Configuración de timeouts para evitar conexiones colgadas
- **Logs**: Registro de todas las actividades para auditoría

### Buenas Prácticas
- Verificar archivos SSH antes de usar
- Usar conexiones SSH en lugar de contraseñas
- Mantener logs para monitoreo
- Crear backups regularmente

## 🚨 Solución de Problemas

### Problemas Comunes

#### Error: "Archivos SSH faltantes"
```bash
# Verificar que existan los archivos
ls -la vps_njalla_nueva*

# Si no existen, crearlos o copiarlos desde la ubicación correcta
cp /ruta/original/vps_njalla_nueva .
cp /ruta/original/vps_njalla_nueva.pub .
```

#### Error: "VPS no responde al ping"
```bash
# Verificar conectividad de red
ping 8.8.8.8

# Verificar si el VPS está activo
ping 80.78.30.242

# Verificar configuración de red
ip route show
```

#### Error: "Conexión SSH falló"
```bash
# Verificar permisos SSH
chmod 600 vps_njalla_nueva
chmod 644 vps_njalla_nueva.pub

# Probar conexión manual
ssh -i vps_njalla_nueva markmur88@80.78.30.242

# Verificar configuración SSH
cat ~/.ssh/config
```

#### Error: "Permisos denegados"
```bash
# Dar permisos de ejecución a los scripts
chmod +x *.sh

# Verificar permisos del directorio
ls -la
```

### Logs de Depuración
```bash
# Ver logs del gestor
tail -f vps_manager.log

# Ver logs de conexión
tail -f vps_connection.log

# Ver logs SSH del sistema
tail -f /var/log/auth.log
```

## 📞 Comandos de Emergencia

### Acceso Directo al VPS
```bash
# Conexión SSH directa
ssh -i vps_njalla_nueva markmur88@80.78.30.242

# Con configuración SSH
ssh vps-elizaos
```

### Reinicio de Servicios
```bash
# Reinicio manual
ssh vps-elizaos "cd ~/elizaos_completo && ./scripts/levantar_sistema_completo.sh"

# Detener todos los servicios
ssh vps-elizaos "pkill -f elizaos"
```

### Backup de Emergencia
```bash
# Backup manual
ssh vps-elizaos "cd ~ && tar -czf backup_emergencia_$(date +%Y%m%d_%H%M%S).tar.gz elizaos_completo/"

# Descargar backup
scp -i vps_njalla_nueva markmur88@80.78.30.242:~/backup_emergencia_*.tar.gz .
```

## 🎯 Casos de Uso

### Desarrollo Diario
```bash
# 1. Conectar al VPS
./vps_manager.sh connect

# 2. Verificar estado
./vps_manager.sh status

# 3. Subir cambios
./vps_manager.sh upload mi_archivo.py

# 4. Reiniciar servicios
./vps_manager.sh restart
```

### Monitoreo Continuo
```bash
# Iniciar monitoreo automático
./vps_manager.sh continuous

# O usar el script específico
./mantener_conexion_vps.sh auto
```

### Mantenimiento
```bash
# 1. Crear backup
./vps_manager.sh backup

# 2. Verificar logs
./vps_manager.sh logs

# 3. Reiniciar servicios
./vps_manager.sh restart
```

## 📈 Mejoras Futuras

### Funcionalidades Planificadas
- [ ] Interfaz web para gestión
- [ ] Notificaciones por email/SMS
- [ ] Métricas avanzadas de rendimiento
- [ ] Integración con sistemas de monitoreo
- [ ] Backup automático programado
- [ ] Restauración automática de servicios

### Optimizaciones
- [ ] Caché de comandos frecuentes
- [ ] Compresión de transferencias
- [ ] Paralelización de operaciones
- [ ] Configuración por archivo YAML/JSON

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios
4. Probar exhaustivamente
5. Crear pull request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

## 👥 Autores

- **Sistema ElizaOS** - Desarrollo inicial y mantenimiento

## 📞 Soporte

Para soporte técnico o preguntas:

1. Revisar la documentación
2. Verificar logs de error
3. Probar comandos de emergencia
4. Contactar al equipo de desarrollo

---

**¡Disfruta gestionando tu VPS de ElizaOS de forma eficiente y segura! 🚀** 