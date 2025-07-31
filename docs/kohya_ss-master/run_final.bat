@echo off
echo === Ejecutando Kohya SS GUI ===
echo.

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Verificando Python...
python --version

echo Verificando dependencias...
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import transformers; print('Transformers:', transformers.__version__)"

echo.
echo Iniciando GUI...
echo La GUI deberia abrirse en: http://localhost:7860
echo Presiona Ctrl+C para detener
echo.

python kohya_gui.py --listen --port 7860

echo.
echo GUI cerrada.
pause 