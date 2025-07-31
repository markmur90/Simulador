#!/usr/bin/env python3
"""
Script especializado para Tortoise TTS - Novelas y Literatura
Optimizado para manejar contenido literario con capítulos y diálogos
"""

import os
import sys
import re
from pathlib import Path
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
import torch
import torchaudio

# Voces recomendadas para literatura
LITERARY_VOICES = {
    '1': ('tom', 'Voz masculina clara - Ideal para narración'),
    '2': ('emma', 'Voz femenina suave - Perfecta para diálogos femeninos'),
    '3': ('daniel', 'Voz masculina profesional - Narrador formal'),
    '4': ('halle', 'Voz femenina clara - Diálogos expresivos'),
    '5': ('freeman', 'Voz masculina profunda - Narración dramática'),
    '6': ('lj', 'Voz femenina natural - Conversaciones íntimas'),
    '7': ('geralt', 'Voz masculina característica - Personajes únicos'),
    '8': ('jlaw', 'Voz femenina elegante - Diálogos sofisticados'),
    '9': ('random', 'Voz aleatoria - Variedad en la narración')
}

# Presets optimizados para literatura
LITERARY_PRESETS = {
    '1': ('ultra_fast', 'Muy rápida - Para pruebas'),
    '2': ('fast', 'Rápida - Buena calidad, tiempo razonable'),
    '3': ('standard', 'Normal - Calidad profesional'),
    '4': ('high_quality', 'Excelente - Para producción final')
}

def print_literary_menu(title, options):
    """Imprime un menú con descripciones detalladas"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")
    for key, (value, description) in options.items():
        print(f" {key}. {value} - {description}")
    print(f"{'='*60}")

def get_literary_choice(options, prompt="Selecciona una opción: "):
    """Obtiene la selección del usuario para menús literarios"""
    while True:
        try:
            choice = input(prompt).strip()
            if choice in options:
                return options[choice][0]  # Retorna solo el valor, no la descripción
            else:
                print(f"❌ Opción inválida. Por favor selecciona un número entre 1 y {len(options)}")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)

def clean_literary_text(text):
    """Limpia y prepara el texto literario para TTS"""
    # Remover caracteres especiales del inicio
    text = re.sub(r'🖋️.*?["\']', '', text)
    
    # Limpiar líneas vacías múltiples
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Asegurar que los diálogos tengan espacios apropiados
    text = re.sub(r'—([^—\n]+)—', r' — \1 — ', text)
    
    return text.strip()

def split_literary_text(text, max_chars=400):
    """Divide texto literario respetando capítulos, diálogos y estructura"""
    text = clean_literary_text(text)
    
    # Detectar capítulos
    chapters = []
    current_chapter = ""
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if re.match(r'^Capítulo\s+[IVX]+', line) or line.startswith('Capítulo'):
            if current_chapter:
                chapters.append(current_chapter.strip())
            current_chapter = line + '\n'
        else:
            current_chapter += line + '\n'
    
    if current_chapter:
        chapters.append(current_chapter.strip())
    
    # Si no hay capítulos claros, dividir por párrafos
    if len(chapters) <= 1:
        paragraphs = text.split('\n\n')
        chunks = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Si el párrafo es muy largo, dividirlo
            if len(paragraph) > max_chars:
                sentences = paragraph.split('.')
                current_chunk = ""
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(current_chunk + sentence + ".") > max_chars and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + "."
                    else:
                        current_chunk += sentence + "." if current_chunk else sentence + "."
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
            else:
                chunks.append(paragraph)
        
        return chunks
    
    # Procesar capítulos
    all_chunks = []
    for i, chapter in enumerate(chapters, 1):
        chapter_lines = chapter.split('\n')
        chapter_title = chapter_lines[0]
        chapter_content = '\n'.join(chapter_lines[1:])
        
        # Dividir el contenido del capítulo
        paragraphs = chapter_content.split('\n\n')
        
        for j, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Si el párrafo es muy largo, dividirlo
            if len(paragraph) > max_chars:
                sentences = paragraph.split('.')
                current_chunk = chapter_title + "\n\n"
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    if len(current_chunk + sentence + ".") > max_chars and current_chunk != chapter_title + "\n\n":
                        all_chunks.append(current_chunk.strip())
                        current_chunk = chapter_title + "\n\n" + sentence + "."
                    else:
                        current_chunk += sentence + "." if current_chunk != chapter_title + "\n\n" else sentence + "."
                
                if current_chunk.strip() != chapter_title + "\n\n":
                    all_chunks.append(current_chunk.strip())
            else:
                chunk = chapter_title + "\n\n" + paragraph
                all_chunks.append(chunk)
    
    return all_chunks

def process_literary_file(file_path, tts, voice_samples, preset, output_dir):
    """Procesa un archivo literario completo"""
    print(f"\n📖 Leyendo novela: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Dividir el texto literario
    chunks = split_literary_text(text)
    print(f"📝 Novela dividida en {len(chunks)} fragmentos")
    
    # Crear directorio de salida
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesar cada fragmento
    for i, chunk in enumerate(chunks, 1):
        print(f"\n🎵 Procesando fragmento {i}/{len(chunks)}...")
        
        # Mostrar el título del capítulo si existe
        lines = chunk.split('\n')
        if lines and 'Capítulo' in lines[0]:
            print(f"📚 {lines[0]}")
        
        # Mostrar una vista previa del contenido
        preview = chunk.replace('\n', ' ')[:80]
        print(f"📄 Vista previa: {preview}...")
        
        try:
            # Generar audio
            audio = tts.tts_with_preset(chunk, voice_samples=voice_samples, preset=preset)
            
            # Guardar archivo con nombre descriptivo
            if 'Capítulo' in chunk:
                chapter_match = re.search(r'Capítulo\s+([IVX]+)', chunk)
                if chapter_match:
                    chapter_num = chapter_match.group(1)
                    output_file = os.path.join(output_dir, f"capitulo_{chapter_num}_fragmento_{i:02d}.wav")
                else:
                    output_file = os.path.join(output_dir, f"fragmento_{i:03d}.wav")
            else:
                output_file = os.path.join(output_dir, f"fragmento_{i:03d}.wav")
            
            torchaudio.save(output_file, audio.squeeze(0).cpu(), 22050)
            print(f"✅ Guardado: {output_file}")
            
        except Exception as e:
            print(f"❌ Error al procesar fragmento {i}: {e}")
            continue
    
    print(f"\n🎉 ¡Novela convertida exitosamente!")
    print(f"📁 Archivos guardados en: {output_dir}")
    print(f"📊 Total de fragmentos procesados: {len(chunks)}")

def main():
    print("📚 Tortoise TTS - Conversor de Novelas")
    print("=" * 50)
    print("Especializado para contenido literario y novelas")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('tortoise'):
        print("❌ Error: Debes ejecutar este script desde el directorio tortoise-tts-main")
        print("💡 Ejecuta: cd C:\\projects\\tortoise-tts-main")
        return
    
    # Seleccionar voz literaria
    print_literary_menu("Voces Recomendadas para Literatura", LITERARY_VOICES)
    selected_voice = get_literary_choice(LITERARY_VOICES, "Selecciona una voz (1-9): ")
    
    # Seleccionar preset literario
    print_literary_menu("Presets Optimizados para Literatura", LITERARY_PRESETS)
    selected_preset = get_literary_choice(LITERARY_PRESETS, "Selecciona un preset (1-4): ")
    
    # Seleccionar archivo literario
    print("\n📁 Selección de archivo literario:")
    print("1. Ingresar ruta del archivo")
    print("2. Usar 'Entre puertas y promesas'")
    print("3. Usar archivo de ejemplo")
    
    file_choice = input("Selecciona una opción (1-3): ").strip()
    
    if file_choice == "1":
        file_path = input("Ingresa la ruta completa del archivo: ").strip()
        if not os.path.exists(file_path):
            print(f"❌ El archivo no existe: {file_path}")
            return
    elif file_choice == "2":
        file_path = "dialogo/texto/Entre_puerta.txt"
        if not os.path.exists(file_path):
            print(f"❌ El archivo no existe: {file_path}")
            print("💡 Asegúrate de que el archivo esté en: dialogo/texto/Entre_puerta.txt")
            return
        print(f"📖 Usando: {file_path}")
    elif file_choice == "3":
        example_files = [
            "tortoise/data/riding_hood.txt",
            "tortoise/data/layman.txt",
            "tortoise/data/got.txt"
        ]
        
        print("\n📄 Archivos de ejemplo disponibles:")
        for i, file in enumerate(example_files, 1):
            if os.path.exists(file):
                print(f" {i}. {file}")
        
        example_choice = input("Selecciona un archivo de ejemplo: ").strip()
        try:
            file_path = example_files[int(example_choice) - 1]
        except:
            print("❌ Opción inválida")
            return
    else:
        print("❌ Opción inválida")
        return
    
    # Configurar directorio de salida
    output_dir = input("Ingresa el directorio de salida (Enter para usar 'novela_audio'): ").strip()
    if not output_dir:
        output_dir = "novela_audio"
    
    print(f"\n⚙️ Configuración para Literatura:")
    print(f"   🎭 Voz: {selected_voice}")
    print(f"   ⚙️ Preset: {selected_preset}")
    print(f"   📖 Archivo: {file_path}")
    print(f"   📁 Salida: {output_dir}")
    
    confirm = input("\n¿Continuar con la conversión? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Inicializar TTS
    print("\n🚀 Inicializando Tortoise TTS para literatura...")
    try:
        tts = TextToSpeech()
        
        # Cargar muestras de voz
        if selected_voice == 'random':
            voice_samples = None
        else:
            voice_samples = load_voice(selected_voice)
        
        # Procesar archivo literario
        process_literary_file(file_path, tts, voice_samples, selected_preset, output_dir)
        
    except Exception as e:
        print(f"❌ Error al inicializar TTS: {e}")
        print("💡 Asegúrate de tener una conexión a internet estable para descargar los modelos")

if __name__ == "__main__":
    main() 