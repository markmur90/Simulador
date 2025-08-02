# Script para organizar todos los archivos de ElizaOS en una sola carpeta
Write-Host "Organizando archivos de ElizaOS..." -ForegroundColor Green

# Crear carpeta principal
$carpetaPrincipal = "elizaos_solucion_completa"
New-Item -ItemType Directory -Path $carpetaPrincipal -Force | Out-Null

# Crear subcarpetas
$subcarpetas = @("scripts", "configs", "docs", "soluciones")
foreach ($carpeta in $subcarpetas) {
    New-Item -ItemType Directory -Path "$carpetaPrincipal\$carpeta" -Force | Out-Null
}

Write-Host "1. Copiando scripts..." -ForegroundColor Yellow

# Scripts principales
$scripts = @(
    "solucionar_base_datos.sh",
    "solucion_manual_elizaos.sh",
    "subir_elizaos_completo.ps1",
    "subir_elizaos_simple.ps1",
    "ejecutar_solucion_completa.ps1",
    "subir_script_solucion.ps1",
    "organizar_elizaos.ps1"
)

foreach ($script in $scripts) {
    if (Test-Path $script) {
        Copy-Item $script "$carpetaPrincipal\scripts\" -Force
        Write-Host "   ✅ $script" -ForegroundColor Green
    }
}

Write-Host "2. Copiando configuraciones..." -ForegroundColor Yellow

# Configuraciones
if (Test-Path "elizaos_completo") {
    Copy-Item "elizaos_completo\configs\*" "$carpetaPrincipal\configs\" -Recurse -Force
    Write-Host "   ✅ Configuraciones de elizaos_completo" -ForegroundColor Green
}

Write-Host "3. Copiando documentación..." -ForegroundColor Yellow

# Documentación
$docs = @(
    "comandos_manuales_vps.txt",
    "solucion_final_elizaos.txt"
)

foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Copy-Item $doc "$carpetaPrincipal\docs\" -Force
        Write-Host "   ✅ $doc" -ForegroundColor Green
    }
}

Write-Host "4. Copiando soluciones..." -ForegroundColor Yellow

# Soluciones específicas
$soluciones = @(
    "reiniciar_elizaos_simple.bat"
)

foreach ($solucion in $soluciones) {
    if (Test-Path $solucion) {
        Copy-Item $solucion "$carpetaPrincipal\soluciones\" -Force
        Write-Host "   ✅ $solucion" -ForegroundColor Green
    }
}

Write-Host "5. Creando README principal..." -ForegroundColor Yellow

# Crear README principal
$readme = @"
# 🚀 ElizaOS - Solución Completa

Carpeta que contiene todos los archivos y soluciones para ElizaOS.

## 📁 Estructura

```
elizaos_solucion_completa/
├── scripts/           # Scripts de instalación y solución
├── configs/           # Configuraciones de ElizaOS
├── docs/              # Documentación y comandos manuales
├── soluciones/        # Soluciones específicas
└── README.md          # Este archivo
```

## 🎯 Problemas Solucionados

- ✅ **Bucle infinito eliminado** - El agente ya no muestra la ayuda en bucle
- ✅ **Comando correcto implementado** - Ahora usa `-- start` para iniciar el servidor
- 🔧 **Base de datos identificada** - Problema con PGLite corrupta

## 🚀 Uso Rápido

### 1. Conectar al VPS
```bash
ssh -i vps_njalla_nueva markmur88@80.78.30.242
```

### 2. Ejecutar solución manual
Ver archivo: `docs/comandos_manuales_vps.txt`

### 3. URLs de acceso
- http://amara.coretransapi.com:9190
- http://80.78.30.242:9190

## 📋 Archivos Importantes

- **`docs/comandos_manuales_vps.txt`** - Comandos para ejecutar en el VPS
- **`scripts/solucionar_base_datos.sh`** - Script para recrear la base de datos
- **`configs/`** - Configuraciones de ElizaOS

## 🎉 Estado Final

Una vez ejecutados los comandos manuales, ElizaOS estará completamente funcional con:
- Todos los módulos locales (Stable Diffusion, SadTalker, etc.)
- Sin necesidad de APIs externas
- Agente completo en puerto 9190
"@

$readme | Out-File "$carpetaPrincipal\README.md" -Encoding UTF8

Write-Host "6. Verificando estructura..." -ForegroundColor Yellow
Get-ChildItem $carpetaPrincipal -Recurse | Select-Object FullName

Write-Host ""
Write-Host "🎉 ¡Organización completada!" -ForegroundColor Green
Write-Host "📁 Carpeta creada: $carpetaPrincipal" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Para usar:" -ForegroundColor Yellow
Write-Host "   1. Revisar docs/comandos_manuales_vps.txt" -ForegroundColor White
Write-Host "   2. Conectar al VPS y ejecutar los comandos" -ForegroundColor White
Write-Host "   3. Acceder a http://amara.coretransapi.com:9190" -ForegroundColor White 