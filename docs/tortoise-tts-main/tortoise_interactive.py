#!/usr/bin/env python3
"""
Script interactivo para Tortoise TTS
Permite elegir opciones por lista y manejar archivos de texto largos
"""

import os
import sys
import argparse
import textwrap
from pathlib import Path
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices
import torch
import torchaudio

# Voces disponibles
VOICES = {
    '1': 'tom',
    '2': 'emma', 
    '3': 'daniel',
    '4': 'freeman',
    '5': 'geralt',
    '6': 'halle',
    '7': 'jlaw',
    '8': 'lj',
    '9': 'mol',
    '10': 'myself',
    '11': 'pat',
    '12': 'rainbow',
    '13': 'snakes',
    '14': 'tim_reynolds',
    '15': 'weaver',
    '16': 'william',
    '17': 'angie',
    '18': 'applejack',
    '19': 'deniro',
    '20': 'random'
}

# Presets disponibles
PRESETS = {
    '1': 'ultra_fast',
    '2': 'fast', 
    '3': 'standard',
    '4': 'high_quality'
}

def print_menu(title, options):
    """Imprime un menú con opciones numeradas"""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")
    for key, value in options.items():
        print(f" {key}. {value}")
    print(f"{'='*50}")

def get_user_choice(options, prompt="Selecciona una opción: "):
    """Obtiene la selección del usuario"""
    while True:
        try:
            choice = input(prompt).strip()
            if choice in options:
                return options[choice]
            else:
                print(f"❌ Opción inválida. Por favor selecciona un número entre 1 y {len(options)}")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)

def split_text_into_chunks(text, max_chars=500):
    """Divide el texto en chunks manejables, respetando capítulos y diálogos"""
    # Limpiar el texto de caracteres especiales al inicio
    text = text.replace('🖋️ Borrador completo: "Entre puertas y promesas"', '').strip()
    
    # Dividir por capítulos primero
    chapters = []
    current_chapter = ""
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('Capítulo'):
            if current_chapter:
                chapters.append(current_chapter.strip())
            current_chapter = line + '\n'
        else:
            current_chapter += line + '\n'
    
    if current_chapter:
        chapters.append(current_chapter.strip())
    
    # Si no hay capítulos claros, dividir por oraciones
    if len(chapters) <= 1:
        sentences = text.replace('\n', ' ').split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Si la oración es muy larga, dividirla
            if len(sentence) > max_chars:
                words = sentence.split()
                temp_chunk = ""
                for word in words:
                    if len(temp_chunk + " " + word) <= max_chars:
                        temp_chunk += " " + word if temp_chunk else word
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = word
                if temp_chunk:
                    current_chunk = temp_chunk
            else:
                # Si agregar esta oración excede el límite, guardar el chunk actual
                if len(current_chunk + ". " + sentence) > max_chars and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += ". " + sentence if current_chunk else sentence
        
        # Agregar el último chunk si existe
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    # Si hay capítulos, dividir cada capítulo en chunks más pequeños
    all_chunks = []
    for i, chapter in enumerate(chapters, 1):
        chapter_title = f"Capítulo {i}"
        if chapter.startswith('Capítulo'):
            chapter_title = chapter.split('\n')[0]
        
        # Dividir el capítulo en oraciones
        chapter_text = chapter.replace(chapter_title, '').strip()
        sentences = chapter_text.split('.')
        
        current_chunk = chapter_title + "\n"
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            if len(current_chunk + sentence + ".") > max_chars:
                if current_chunk.strip() != chapter_title:
                    all_chunks.append(current_chunk.strip())
                current_chunk = chapter_title + "\n" + sentence + "."
            else:
                current_chunk += sentence + "."
        
        if current_chunk.strip() != chapter_title:
            all_chunks.append(current_chunk.strip())
    
    return all_chunks

def process_text_file(file_path, tts, voice_samples, preset, output_dir):
    """Procesa un archivo de texto completo"""
    print(f"\n📖 Leyendo archivo: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Dividir el texto en chunks
    chunks = split_text_into_chunks(text)
    print(f"📝 Texto dividido en {len(chunks)} chunks")
    
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesar cada chunk
    for i, chunk in enumerate(chunks, 1):
        print(f"\n🎵 Procesando chunk {i}/{len(chunks)}...")
        print(f"📄 Texto: {chunk[:100]}{'...' if len(chunk) > 100 else ''}")
        
        try:
            # Generar audio
            audio = tts.tts_with_preset(chunk, voice_samples=voice_samples, preset=preset)
            
            # Guardar archivo
            output_file = os.path.join(output_dir, f"chunk_{i:03d}.wav")
            torchaudio.save(output_file, audio.squeeze(0).cpu(), 22050)
            print(f"✅ Guardado: {output_file}")
            
        except Exception as e:
            print(f"❌ Error al procesar chunk {i}: {e}")
            continue
    
    print(f"\n🎉 ¡Procesamiento completado! Archivos guardados en: {output_dir}")

def main():
    print("🎤 Tortoise TTS - Script Interactivo")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('tortoise'):
        print("❌ Error: Debes ejecutar este script desde el directorio tortoise-tts-main")
        print("💡 Ejecuta: cd C:\\projects\\tortoise-tts-main")
        return
    
    # Seleccionar voz
    print_menu("Voces Disponibles", VOICES)
    selected_voice = get_user_choice(VOICES, "Selecciona una voz (1-20): ")
    
    # Seleccionar preset
    print_menu("Presets de Calidad", PRESETS)
    selected_preset = get_user_choice(PRESETS, "Selecciona un preset (1-4): ")
    
    # Seleccionar archivo de texto
    print("\n📁 Selección de archivo de texto:")
    print("1. Ingresar ruta del archivo")
    print("2. Usar archivo de ejemplo")
    print("3. Usar 'Entre puertas y promesas'")
    
    file_choice = input("Selecciona una opción (1-3): ").strip()
    
    if file_choice == "1":
        file_path = input("Ingresa la ruta completa del archivo de texto: ").strip()
        if not os.path.exists(file_path):
            print(f"❌ El archivo no existe: {file_path}")
            return
    elif file_choice == "2":
        # Usar archivo de ejemplo
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
    elif file_choice == "3":
        # Usar el archivo de diálogo específico
        file_path = "dialogo/texto/Entre_puerta.txt"
        if not os.path.exists(file_path):
            print(f"❌ El archivo no existe: {file_path}")
            print("💡 Asegúrate de que el archivo esté en la ruta: dialogo/texto/Entre_puerta.txt")
            return
        print(f"📖 Usando: {file_path}")
    else:
        print("❌ Opción inválida")
        return
    
    # Configurar directorio de salida
    output_dir = input("Ingresa el directorio de salida (Enter para usar 'output'): ").strip()
    if not output_dir:
        output_dir = "output"
    
    print(f"\n⚙️ Configuración:")
    print(f"   Voz: {selected_voice}")
    print(f"   Preset: {selected_preset}")
    print(f"   Archivo: {file_path}")
    print(f"   Salida: {output_dir}")
    
    confirm = input("\n¿Continuar? (s/n): ").strip().lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada")
        return
    
    # Inicializar TTS
    print("\n🚀 Inicializando Tortoise TTS...")
    try:
        tts = TextToSpeech()
        
        # Cargar muestras de voz
        if selected_voice == 'random':
            voice_samples = None
        else:
            voice_samples = load_voice(selected_voice)
        
        # Procesar archivo
        process_text_file(file_path, tts, voice_samples, selected_preset, output_dir)
        
    except Exception as e:
        print(f"❌ Error al inicializar TTS: {e}")
        print("💡 Asegúrate de tener una conexión a internet estable para descargar los modelos")

if __name__ == "__main__":
    main() 