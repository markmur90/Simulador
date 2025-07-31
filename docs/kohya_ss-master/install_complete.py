#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

def run_command(cmd, description):
    print(f"Ejecutando: {description}")
    print(f"Comando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completado")
            if result.stdout:
                print(f"Salida: {result.stdout}")
        else:
            print(f"✗ {description} falló")
            if result.stderr:
                print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"✗ {description} falló con excepción: {e}")
        return False

def main():
    print("=== Instalación Completa de Kohya SS ===")
    print(f"Python version: {sys.version}")
    print(f"Directorio actual: {os.getcwd()}")
    
    # Paso 1: Crear entorno virtual
    if not run_command("python -m venv venv_final", "Crear entorno virtual"):
        return False
    
    # Paso 2: Activar entorno virtual
    if os.name == 'nt':  # Windows
        activate_cmd = "venv_final\\Scripts\\activate.bat && "
    else:  # Linux/Mac
        activate_cmd = "source venv_final/bin/activate && "
    
    # Paso 3: Actualizar pip
    if not run_command(f"{activate_cmd}python -m pip install --upgrade pip setuptools wheel", "Actualizar pip"):
        return False
    
    # Paso 4: Instalar PyTorch
    if not run_command(f"{activate_cmd}pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118", "Instalar PyTorch"):
        return False
    
    # Paso 5: Instalar dependencias básicas
    basic_deps = [
        "accelerate", "diffusers", "transformers", "safetensors", 
        "omegaconf", "pytorch-lightning", "rich", "ftfy", "einops", 
        "opencv-python", "scipy", "timm", "huggingface-hub", 
        "wandb", "gradio", "easygui"
    ]
    
    for dep in basic_deps:
        if not run_command(f"{activate_cmd}pip install {dep}", f"Instalar {dep}"):
            print(f"Advertencia: No se pudo instalar {dep}")
    
    # Paso 6: Instalar dependencias adicionales
    extra_deps = [
        "lycoris_lora", "dadaptation", "lion-pytorch", "prodigyopt", 
        "prodigy-plus-schedule-free", "schedulefree", "pytorch-optimizer", 
        "fairscale", "aiofiles", "altair", "imagesize", "invisible-watermark", 
        "open-clip-torch", "onnx", "protobuf", "sentencepiece", "tk", 
        "toml", "voluptuous"
    ]
    
    for dep in extra_deps:
        if not run_command(f"{activate_cmd}pip install {dep}", f"Instalar {dep}"):
            print(f"Advertencia: No se pudo instalar {dep}")
    
    # Paso 7: Instalar sd-scripts
    if not run_command(f"{activate_cmd}pip install -e ./sd-scripts", "Instalar sd-scripts"):
        print("Advertencia: No se pudo instalar sd-scripts")
    
    # Paso 8: Verificar instalación
    print("\n=== Verificando instalación ===")
    test_imports = [
        "torch", "diffusers", "transformers", "gradio", 
        "accelerate", "safetensors", "omegaconf"
    ]
    
    for module in test_imports:
        if not run_command(f"{activate_cmd}python -c \"import {module}; print('✓ {module} OK')\"", f"Verificar {module}"):
            print(f"✗ {module} no está disponible")
    
    print("\n=== Instalación completada ===")
    print("Para ejecutar la GUI, usa:")
    print("venv_final\\Scripts\\activate.bat && python kohya_gui.py --listen --port 7860")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("✓ Instalación exitosa")
    else:
        print("✗ Instalación falló")
        sys.exit(1) 