# 🚀 ElizaOS - Sistema Completo de Inteligencia Artificial

## 📋 Descripción General

ElizaOS es un sistema completo de inteligencia artificial que funciona 100% localmente, sin dependencias de APIs externas. Incluye múltiples agentes especializados, módulos de generación de imágenes, procesamiento de texto y herramientas de desarrollo.

## 🏗️ Arquitectura del Proyecto

```
elizaos/
├── 📁 comandos/                    # Scripts de gestión y automatización
│   ├── PowerShell scripts (.ps1)   # Automatización Windows
│   ├── Bash scripts (.sh)          # Automatización Linux
│   ├── Batch files (.bat)          # Comandos Windows
│   └── Documentación de comandos
├── 📁 elizaos_completo/            # Sistema principal de ElizaOS
│   ├── scripts/                    # Scripts de instalación
│   ├── configs/                    # Configuraciones
│   └── agentes_elizaos/            # Sistema de agentes
├── 📁 agentes_elizaos/             # Sistema de gestión de agentes
│   ├── templates/                  # Templates JSON para agentes
│   ├── scripts/                    # Scripts de gestión
│   ├── configs/                    # Configuraciones
│   └── docs/                       # Documentación
└── 📁 elizaos_solucion_completa/   # Soluciones y troubleshooting
    ├── scripts/                    # Scripts de solución
    ├── configs/                    # Configuraciones
    ├── docs/                       # Documentación
    └── soluciones/                 # Soluciones específicas
```

## 🌟 Características Principales

### ✅ Funcionalidades Core
- **100% Local**: Sin dependencias de APIs externas
- **Múltiples Agentes**: Sistema de agentes especializados
- **Generación de Imágenes**: Integración con Stable Diffusion
- **Procesamiento de Texto**: Modelos locales de IA
- **Base de Datos**: PGLite integrada
- **Gestión de Procesos**: PM2 para reinicio automático

### 🤖 Agentes Disponibles
1. **Agente Completo** (Puerto 9190) - Todos los módulos
2. **Desarrollador Web** (Puerto 9183) - Programación
3. **Escritor Creativo** (Puerto 9184) - Contenido
4. **Analista de Datos** (Puerto 9185) - Business Intelligence
5. **Soporte al Cliente** (Puerto 9186) - Atención
6. **Marketing** (Puerto 9187) - Estrategias

### 🔧 Módulos Integrados
- **Stable Diffusion**: Generación de imágenes
- **SadTalker**: Generación de videos
- **Thor Toys**: Herramientas de desarrollo
- **HuggingFace**: Modelos de lenguaje
- **SQL**: Gestión de base de datos

## 🚀 Inicio Rápido

### Para Windows
```powershell
# Ver README_Windows.md para instrucciones detalladas
cd comandos
.\organizar_elizaos.ps1
.\subir_elizaos_completo.ps1
```

### Para Linux
```bash
# Ver README_Linux.md para instrucciones detalladas
cd comandos
chmod +x *.sh
./subir_elizaos_completo.sh
```

### En el VPS (Después de subir archivos)
```bash
ssh -i vps_njalla_nueva markmur88@80.78.30.242
cd ~/elizaos_completo
./scripts/instalacion_completa.sh
```

## 🌐 URLs de Acceso

- **Agente Principal**: http://amara.coretransapi.com:9190
- **Agente Básico**: http://amara.coretransapi.com:9182
- **Agentes Especializados**: http://amara.coretransapi.com:9183-9187

## 📋 Flujo de Trabajo Completo

### 1. Preparación Local
```bash
# Organizar archivos
./comandos/organizar_elizaos.ps1

# Subir al VPS
./comandos/subir_elizaos_completo.ps1
```

### 2. Instalación en VPS
```bash
# Conectar al VPS
ssh -i vps_njalla_nueva markmur88@80.78.30.242

# Instalación completa
cd ~/elizaos_completo
./scripts/instalacion_completa.sh
```

### 3. Gestión de Agentes
```bash
# Ver agentes activos
cd ~/elizaos_completo/agentes_elizaos
./scripts/gestionar_agentes.sh list

# Crear nuevo agente
./scripts/crear_agente_template.sh agente_completo_local mi-agente 9190

# Reiniciar agente
./scripts/gestionar_agentes.sh restart mi-agente
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
PORT=9190
HOST=0.0.0.0
USE_LOCAL_MODULES=true
NO_EXTERNAL_APIS=true
PGLITE_DATA_DIR=/home/markmur88/eliza-develop/.eliza
LOG_LEVEL=info
```

### Configuración de Agente
```json
{
  "name": "amara-complete",
  "plugins": [
    "@elizaos/plugin-bootstrap",
    "@elizaos/plugin-dummy-services",
    "@elizaos/plugin-sql"
  ],
  "settings": {
    "port": 9190,
    "local_modules": {
      "gaby_fullstack": {
        "enabled": true,
        "models": {
          "stable_diffusion": {"enabled": true},
          "huggingface": {"enabled": true}
        }
      }
    }
  }
}
```

## 🛠️ Troubleshooting

### Problemas Comunes

#### Base de Datos Corrupta
```bash
# Solución automática
./comandos/solucionar_base_datos.sh

# Solución manual
pm2 stop amara-complete
rm -rf ~/eliza-develop/.eliza
mkdir -p ~/eliza-develop/.eliza
pm2 start dist/index.js --name 'amara-complete' -- start
```

#### Puerto en Uso
```bash
# Verificar puertos
netstat -tlnp | grep :9190

# Solucionar conflicto
./agentes_elizaos/scripts/solucionar_puerto_9182.sh
```

#### Agente No Inicia
```bash
# Diagnóstico completo
./agentes_elizaos/scripts/diagnostico_completo.sh

# Ver logs
pm2 logs amara-complete --lines 20
```

## 📊 Monitoreo y Mantenimiento

### Comandos Útiles
```bash
# Ver estado de agentes
pm2 list

# Ver logs en tiempo real
pm2 logs amara-complete

# Reiniciar todos los agentes
pm2 restart all

# Ver uso de recursos
pm2 monit
```

### Verificación de Estado
```bash
# Verificar puertos
netstat -tlnp | grep -E ':(918[2-7]|919[0-1])'

# Verificar firewall
sudo ufw status

# Verificar servicios
systemctl status pm2-markmur88
```

## 📚 Documentación Adicional

- **[README_Windows.md](README_Windows.md)** - Guía específica para Windows
- **[README_Linux.md](README_Linux.md)** - Guía específica para Linux
- **[comandos/README_VPS_SCRIPTS.md](comandos/README_VPS_SCRIPTS.md)** - Documentación de scripts VPS
- **[agentes_elizaos/docs/](agentes_elizaos/docs/)** - Documentación del sistema de agentes

## 🎯 Casos de Uso

### Desarrollo Web
```bash
# Crear agente desarrollador
./scripts/crear_agente_template.sh agente_web_developer dev-agent 9183
```

### Análisis de Datos
```bash
# Crear agente analista
./scripts/crear_agente_template.sh agente_data_analyst data-agent 9185
```

### Marketing
```bash
# Crear agente marketing
./scripts/crear_agente_template.sh agente_marketing marketing-agent 9187
```

## 🔒 Seguridad

- **Firewall UFW**: Configurado automáticamente
- **Puertos Específicos**: Solo puertos necesarios abiertos
- **Sin APIs Externas**: 100% local para mayor seguridad
- **Logs Detallados**: Monitoreo completo de actividad

## 📈 Rendimiento

- **PM2**: Gestión de procesos y reinicio automático
- **Módulos Locales**: Sin latencia de red
- **Base de Datos Optimizada**: PGLite para mejor rendimiento
- **Recursos Optimizados**: Configuración para VPS

## 🤝 Contribución

Para contribuir al proyecto:

1. Revisar la estructura de carpetas
2. Seguir las convenciones de nomenclatura
3. Documentar cambios en README correspondiente
4. Probar en entorno de desarrollo antes de producción

## 📞 Soporte

- **Documentación**: Revisar archivos README específicos
- **Troubleshooting**: Usar scripts de diagnóstico
- **Logs**: Verificar logs de PM2 para errores
- **Comandos Manuales**: Ver `comandos/comandos_manuales_vps.txt`

---

## 🎉 ¡ElizaOS está Listo para Usar!

Con esta configuración tienes un sistema completo de IA que incluye:
- ✅ Instalación automatizada
- ✅ Múltiples agentes especializados
- ✅ Módulos locales integrados
- ✅ Gestión de procesos robusta
- ✅ Documentación completa
- ✅ Scripts de mantenimiento

**¡Tu sistema ElizaOS está completamente operativo y listo para cualquier tarea de IA!** 