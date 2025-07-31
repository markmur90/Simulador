@echo off
echo === Instalacion Completa de Kohya SS ===

echo Creando entorno virtual...
python -m venv venv_final

echo Activando entorno virtual...
call venv_final\Scripts\activate.bat

echo Actualizando pip...
python -m pip install --upgrade pip setuptools wheel

echo Instalando PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo Instalando dependencias basicas...
pip install accelerate diffusers transformers safetensors omegaconf pytorch-lightning rich ftfy einops opencv-python scipy timm huggingface-hub wandb gradio easygui

echo Instalando dependencias adicionales...
pip install lycoris_lora dadaptation lion-pytorch prodigyopt prodigy-plus-schedule-free schedulefree pytorch-optimizer fairscale aiofiles altair imagesize invisible-watermark open-clip-torch onnx protobuf sentencepiece tk toml voluptuous

echo Instalando sd-scripts...
pip install -e ./sd-scripts

echo === Instalacion completada ===
echo Para ejecutar la GUI, usa:
echo venv_final\Scripts\activate.bat ^&^& python kohya_gui.py --listen --port 7860

pause 