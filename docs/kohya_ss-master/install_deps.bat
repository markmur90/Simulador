@echo off
echo === Instalando dependencias faltantes ===

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias basicas...
pip install toml transformers diffusers accelerate safetensors omegaconf pytorch-lightning rich ftfy einops opencv-python scipy timm huggingface-hub wandb gradio easygui

echo Instalando dependencias adicionales...
pip install lycoris_lora dadaptation lion-pytorch prodigyopt prodigy-plus-schedule-free schedulefree pytorch-optimizer fairscale aiofiles altair imagesize invisible-watermark open-clip-torch onnx protobuf sentencepiece tk voluptuous

echo Instalando sd-scripts...
pip install -e ./sd-scripts

echo Verificando instalacion...
python -c "import toml; print('✓ toml OK')"
python -c "import transformers; print('✓ transformers OK')"
python -c "import diffusers; print('✓ diffusers OK')"
python -c "import gradio; print('✓ gradio OK')"

echo === Instalacion completada ===
echo Para ejecutar la GUI:
echo venv\Scripts\activate.bat ^&^& python kohya_gui.py --listen --port 7860

pause 