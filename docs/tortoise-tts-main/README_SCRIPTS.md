# 🎤 Scripts Interactivos para Tortoise TTS

Este directorio contiene scripts interactivos para facilitar el uso de Tortoise TTS.

## 📋 Requisitos

- Tortoise TTS instalado correctamente
- Entorno conda activado: `conda activate tortoise`
- Conexión a internet para descargar modelos

## 🚀 Scripts Disponibles

### 1. `tortoise_interactive.py` - Script Completo Interactivo

**Características:**
- ✅ Menús interactivos con opciones numeradas
- ✅ 20 voces diferentes disponibles
- ✅ 4 presets de calidad
- ✅ Manejo de archivos de texto largos
- ✅ División automática en chunks
- ✅ Archivos de ejemplo incluidos
- ✅ **NUEVO**: Soporte para "Entre puertas y promesas"
- ✅ Directorio de salida personalizable

**Uso:**
```bash
python tortoise_interactive.py
```

**Flujo del script:**
1. Seleccionar voz de la lista
2. Seleccionar preset de calidad
3. Elegir archivo de texto (ruta personalizada, ejemplo, o "Entre puertas y promesas")
4. Configurar directorio de salida
5. Confirmar y procesar

### 2. `tortoise_novel.py` - Script Especializado para Novelas 🆕

**Características:**
- ✅ **Optimizado para literatura y novelas**
- ✅ **Voces recomendadas para narrativa**
- ✅ **Presets optimizados para contenido literario**
- ✅ **División inteligente por capítulos**
- ✅ **Manejo especial de diálogos**
- ✅ **Limpieza automática de texto literario**
- ✅ **Nombres de archivo descriptivos**
- ✅ **Interfaz especializada para escritores**

**Uso:**
```bash
python tortoise_novel.py
```

**Especialmente recomendado para:**
- Novelas y cuentos
- Contenido literario con capítulos
- Textos con diálogos
- "Entre puertas y promesas" y similares

### 3. `tortoise_simple.py` - Script Simple

**Características:**
- ✅ Conversión rápida de texto a audio
- ✅ Configuración por defecto o personalizada
- ✅ Ideal para textos cortos
- ✅ Interfaz simple

**Uso:**
```bash
python tortoise_simple.py
```

## 🎭 Voces Disponibles

### Voces Generales (tortoise_interactive.py)
| Número | Voz | Descripción |
|--------|-----|-------------|
| 1 | tom | Voz masculina clara |
| 2 | emma | Voz femenina suave |
| 3 | daniel | Voz masculina profesional |
| 4 | freeman | Voz masculina profunda |
| 5 | geralt | Voz masculina característica |
| 6 | halle | Voz femenina clara |
| 7 | jlaw | Voz femenina elegante |
| 8 | lj | Voz femenina natural |
| 9 | mol | Voz femenina cálida |
| 10 | myself | Voz personalizada |
| 11 | pat | Voz masculina amigable |
| 12 | rainbow | Voz femenina expresiva |
| 13 | snakes | Voz masculina distintiva |
| 14 | tim_reynolds | Voz masculina profesional |
| 15 | weaver | Voz masculina clara |
| 16 | william | Voz masculina formal |
| 17 | angie | Voz femenina joven |
| 18 | applejack | Voz femenina característica |
| 19 | deniro | Voz masculina distintiva |
| 20 | random | Voz aleatoria |

### Voces Literarias (tortoise_novel.py) 🆕
| Número | Voz | Uso Recomendado |
|--------|-----|-----------------|
| 1 | tom | Narración general |
| 2 | emma | Diálogos femeninos |
| 3 | daniel | Narrador formal |
| 4 | halle | Diálogos expresivos |
| 5 | freeman | Narración dramática |
| 6 | lj | Conversaciones íntimas |
| 7 | geralt | Personajes únicos |
| 8 | jlaw | Diálogos sofisticados |
| 9 | random | Variedad narrativa |

## ⚙️ Presets de Calidad

| Número | Preset | Velocidad | Calidad | Uso Recomendado |
|--------|--------|-----------|---------|-----------------|
| 1 | ultra_fast | Muy rápida | Básica | Pruebas rápidas |
| 2 | fast | Rápida | Buena | Uso diario |
| 3 | standard | Normal | Muy buena | Producción |
| 4 | high_quality | Lenta | Excelente | Producción final |

## 📁 Archivos de Ejemplo

### Archivos Incluidos
- `tortoise/data/riding_hood.txt` - Cuento de Caperucita Roja
- `tortoise/data/layman.txt` - Texto técnico
- `tortoise/data/got.txt` - Fragmento literario

### Archivo Especial 🆕
- `dialogo/texto/Entre_puerta.txt` - "Entre puertas y promesas" (novela romántica)

## 🔧 Uso Avanzado

### Script Interactivo para Archivos Largos
```bash
# Activar entorno
conda activate tortoise

# Navegar al directorio
cd C:\projects\tortoise-tts-main

# Ejecutar script
python tortoise_interactive.py
```

### Script Especializado para Novelas 🆕
```bash
# Activar entorno
conda activate tortoise

# Navegar al directorio
cd C:\projects\tortoise-tts-main

# Ejecutar script literario
python tortoise_novel.py
```

### Script Simple para Textos Cortos
```bash
# Activar entorno
conda activate tortoise

# Navegar al directorio
cd C:\projects\tortoise-tts-main

# Ejecutar script
python tortoise_simple.py
```

## 📂 Estructura de Salida

### Script Interactivo
```
output/
├── chunk_001.wav
├── chunk_002.wav
├── chunk_003.wav
└── ...
```

### Script Especializado para Novelas 🆕
```
novela_audio/
├── capitulo_I_fragmento_01.wav
├── capitulo_I_fragmento_02.wav
├── capitulo_II_fragmento_01.wav
├── capitulo_II_fragmento_02.wav
└── ...
```

### Script Simple
```
output.wav
```

## 📚 Características Especiales para Literatura 🆕

### División Inteligente
- **Respeto a capítulos**: Mantiene la estructura original
- **Diálogos preservados**: No corta en medio de conversaciones
- **Párrafos completos**: Evita cortes abruptos

### Limpieza Automática
- **Caracteres especiales**: Remueve emojis y símbolos
- **Formato de diálogos**: Mejora la legibilidad
- **Espaciado optimizado**: Para mejor narración

### Nombres Descriptivos
- **Capítulos identificados**: `capitulo_I_fragmento_01.wav`
- **Secuencia lógica**: Fácil de organizar
- **Información clara**: Sabes qué contiene cada archivo

## ⚠️ Notas Importantes

1. **Primera ejecución**: La primera vez que ejecutes los scripts, se descargarán los modelos necesarios (puede tomar varios minutos)

2. **Conexión a internet**: Se requiere conexión estable para descargar modelos

3. **GPU recomendada**: Para mejor rendimiento, usa una GPU NVIDIA

4. **Memoria**: Los modelos requieren varios GB de RAM

5. **Tiempo de procesamiento**: 
   - `ultra_fast`: ~30 segundos por chunk
   - `fast`: ~1 minuto por chunk
   - `standard`: ~2 minutos por chunk
   - `high_quality`: ~5 minutos por chunk

6. **Para novelas largas**: Usa `tortoise_novel.py` para mejor manejo de capítulos

## 🐛 Solución de Problemas

### Error de conexión
```
❌ Error al descargar modelos
```
**Solución**: Verifica tu conexión a internet y vuelve a intentar

### Error de memoria
```
❌ CUDA out of memory
```
**Solución**: Usa un preset más rápido o reduce el tamaño del texto

### Error de módulo
```
❌ No module named 'tortoise'
```
**Solución**: Asegúrate de estar en el directorio correcto y con el entorno activado

### Error con archivo de diálogo
```
❌ El archivo no existe: dialogo/texto/Entre_puerta.txt
```
**Solución**: Verifica que el archivo esté en la ruta correcta

## 📞 Soporte

Si encuentras problemas:
1. Verifica que el entorno conda esté activado
2. Asegúrate de estar en el directorio `tortoise-tts-main`
3. Verifica tu conexión a internet
4. Revisa que tengas suficiente espacio en disco
5. Para novelas, usa `tortoise_novel.py` en lugar del script general

## 🎯 Recomendaciones por Uso

### Para Novelas y Literatura
- **Script recomendado**: `tortoise_novel.py`
- **Voz recomendada**: emma, halle, daniel
- **Preset recomendado**: standard o high_quality

### Para Textos Cortos
- **Script recomendado**: `tortoise_simple.py`
- **Preset recomendado**: fast

### Para Pruebas Rápidas
- **Script recomendado**: `tortoise_interactive.py`
- **Preset recomendado**: ultra_fast

¡Disfruta usando Tortoise TTS! 🎤✨ 