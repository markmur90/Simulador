#!/usr/bin/env python3
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Iniciando Kohya SS GUI...")
    print(f"Python version: {sys.version}")
    print(f"Directorio actual: {os.getcwd()}")
    
    # Importar y ejecutar la GUI
    from kohya_gui import UI
    
    print("GUI importada correctamente")
    
    # Configurar argumentos
    kwargs = {
        "listen": "0.0.0.0",
        "server_port": 7860,
        "headless": False,
        "do_not_use_shell": False,
        "config": "config.toml"
    }
    
    print("Iniciando interfaz...")
    UI(**kwargs)
    
except Exception as e:
    print(f"Error al iniciar la GUI: {e}")
    import traceback
    traceback.print_exc() 