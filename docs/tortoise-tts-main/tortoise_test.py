#!/usr/bin/env python3
"""
Script de prueba simple para Tortoise TTS
"""

import os
import sys

def test_imports():
    """Prueba que las importaciones funcionen"""
    try:
        print("🔍 Probando importaciones...")
        from tortoise.api import TextToSpeech
        from tortoise.utils.audio import load_voice
        import torch
        import torchaudio
        print("✅ Todas las importaciones exitosas")
        return True
    except Exception as e:
        print(f"❌ Error en importaciones: {e}")
        return False

def test_tts():
    """Prueba básica de TTS"""
    try:
        print("🎤 Inicializando TTS...")
        from tortoise.api import TextToSpeech
        tts = TextToSpeech()
        print("✅ TTS inicializado correctamente")
        return tts
    except Exception as e:
        print(f"❌ Error al inicializar TTS: {e}")
        return None

def test_simple_generation(tts):
    """Prueba generación simple de audio"""
    try:
        print("🎵 Generando audio de prueba...")
        text = "Hola, esto es una prueba de Tortoise TTS."
        
        # Generar audio
        audio = tts.tts_with_preset(text, preset='ultra_fast')
        
        # Guardar archivo
        output_file = "test_output.wav"
        torchaudio.save(output_file, audio.squeeze(0).cpu(), 22050)
        
        print(f"✅ Audio guardado en: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error al generar audio: {e}")
        return False

def main():
    print("🧪 Tortoise TTS - Script de Prueba")
    print("=" * 40)
    
    # Probar importaciones
    if not test_imports():
        return
    
    # Probar inicialización
    tts = test_tts()
    if not tts:
        return
    
    # Probar generación
    if test_simple_generation(tts):
        print("\n🎉 ¡Todas las pruebas exitosas!")
        print("💡 Tortoise TTS está funcionando correctamente")
    else:
        print("\n❌ Error en las pruebas")

if __name__ == "__main__":
    main() 