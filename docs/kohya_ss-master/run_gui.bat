@echo off
echo Iniciando Kohya SS GUI...
cd /d "%~dp0"
python kohya_gui.py --listen --port 7860
pause 