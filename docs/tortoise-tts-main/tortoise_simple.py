#!/usr/bin/env python3
"""
Script simple para Tortoise TTS
Conversión rápida de texto a audio
"""

import os
import sys
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice
import torch
import torchaudio

def simple_tts(text, voice="tom", preset="fast", output_file="output.wav"):
    """
    Función simple para convertir texto a audio
    """
    print(f"🎤 Convirtiendo texto a audio...")
    print(f"📄 Texto: {text[:100]}{'...' if len(text) > 100 else ''}")
    print(f"🎭 Voz: {voice}")
    print(f"⚙️ Preset: {preset}")
    
    try:
        # Inicializar TTS
        tts = TextToSpeech()
        
        # Cargar voz
        voice_samples = load_voice(voice) if voice != "random" else None
        
        # Generar audio
        audio = tts.tts_with_preset(text, voice_samples=voice_samples, preset=preset)
        
        # Guardar archivo
        torchaudio.save(output_file, audio.squeeze(0).cpu(), 22050)
        print(f"✅ Audio guardado en: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎤 Tortoise TTS - Conversión Simple")
    print("=" * 40)
    
    # Obtener texto del usuario
    print("\n📝 Ingresa el texto que quieres convertir a audio:")
    text = input("Texto: ").strip()
    
    if not text:
        print("❌ No se ingresó texto")
        return
    
    # Opciones rápidas
    print("\n⚙️ Opciones:")
    print("1. Usar configuración por defecto (tom, fast)")
    print("2. Personalizar configuración")
    
    choice = input("Selecciona (1-2): ").strip()
    
    if choice == "1":
        voice = "tom"
        preset = "fast"
        output_file = "output.wav"
    elif choice == "2":
        print("\n🎭 Voces disponibles: tom, emma, daniel, freeman, geralt, halle, jlaw, lj, mol, myself, pat, rainbow, snakes, tim_reynolds, weaver, william, angie, applejack, deniro, random")
        voice = input("Voz (Enter para 'tom'): ").strip() or "tom"
        
        print("\n⚙️ Presets: ultra_fast, fast, standard, high_quality")
        preset = input("Preset (Enter para 'fast'): ").strip() or "fast"
        
        output_file = input("Archivo de salida (Enter para 'output.wav'): ").strip() or "output.wav"
    else:
        print("❌ Opción inválida")
        return
    
    # Ejecutar conversión
    success = simple_tts(text, voice, preset, output_file)
    
    if success:
        print(f"\n🎉 ¡Conversión completada!")
        print(f"📁 Archivo: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    main() 