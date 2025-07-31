#!/usr/bin/env python3
import sys
import os

print("=== Test de Instalación Kohya SS ===")
print(f"Python version: {sys.version}")
print(f"Directorio actual: {os.getcwd()}")

try:
    import torch
    print(f"✓ PyTorch: {torch.__version__}")
    print(f"  CUDA disponible: {torch.cuda.is_available()}")
except ImportError as e:
    print(f"✗ PyTorch: Error - {e}")

try:
    import diffusers
    print(f"✓ Diffusers: {diffusers.__version__}")
except ImportError as e:
    print(f"✗ Diffusers: Error - {e}")

try:
    import transformers
    print(f"✓ Transformers: {transformers.__version__}")
except ImportError as e:
    print(f"✗ Transformers: Error - {e}")

try:
    import gradio
    print(f"✓ Gradio: {gradio.__version__}")
except ImportError as e:
    print(f"✗ Gradio: Error - {e}")

try:
    import accelerate
    print(f"✓ Accelerate: {accelerate.__version__}")
except ImportError as e:
    print(f"✗ Accelerate: Error - {e}")

try:
    import safetensors
    print(f"✓ Safetensors: {safetensors.__version__}")
except ImportError as e:
    print(f"✗ Safetensors: Error - {e}")

try:
    import omegaconf
    print(f"✓ OmegaConf: {omegaconf.__version__}")
except ImportError as e:
    print(f"✗ OmegaConf: Error - {e}")

try:
    import pytorch_lightning
    print(f"✓ PyTorch Lightning: {pytorch_lightning.__version__}")
except ImportError as e:
    print(f"✗ PyTorch Lightning: Error - {e}")

print("\n=== Verificando archivos del proyecto ===")
files_to_check = [
    "kohya_gui.py",
    "requirements.txt",
    "sd-scripts/setup.py",
    "setup/validate_requirements.py"
]

for file in files_to_check:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} - No encontrado")

print("\n=== Fin del test ===") 