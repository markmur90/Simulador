#!/usr/bin/env python3
import sys
import os
import traceback

print("=== Debug de Kohya SS GUI ===")
print(f"Python version: {sys.version}")
print(f"Directorio actual: {os.getcwd()}")

# Verificar imports básicos
try:
    import torch
    print(f"✓ PyTorch: {torch.__version__}")
except Exception as e:
    print(f"✗ PyTorch: {e}")

try:
    import gradio
    print(f"✓ Gradio: {gradio.__version__}")
except Exception as e:
    print(f"✗ Gradio: {e}")

try:
    import transformers
    print(f"✓ Transformers: {transformers.__version__}")
except Exception as e:
    print(f"✗ Transformers: {e}")

try:
    import diffusers
    print(f"✓ Diffusers: {diffusers.__version__}")
except Exception as e:
    print(f"✗ Diffusers: {e}")

# Verificar módulo kohya_gui
try:
    import kohya_gui
    print("✓ Módulo kohya_gui importado")
except Exception as e:
    print(f"✗ Módulo kohya_gui: {e}")
    traceback.print_exc()

# Verificar archivos específicos
try:
    from kohya_gui.class_gui_config import KohyaSSGUIConfig
    print("✓ KohyaSSGUIConfig importado")
except Exception as e:
    print(f"✗ KohyaSSGUIConfig: {e}")
    traceback.print_exc()

try:
    from kohya_gui.dreambooth_gui import dreambooth_tab
    print("✓ dreambooth_tab importado")
except Exception as e:
    print(f"✗ dreambooth_tab: {e}")
    traceback.print_exc()

try:
    from kohya_gui.lora_gui import lora_tab
    print("✓ lora_tab importado")
except Exception as e:
    print(f"✗ lora_tab: {e}")
    traceback.print_exc()

try:
    from kohya_gui.custom_logging import setup_logging
    print("✓ setup_logging importado")
except Exception as e:
    print(f"✗ setup_logging: {e}")
    traceback.print_exc()

print("=== Fin del debug ===") 