# Simulador Bancario

Este repositorio contiene un proyecto Django de ejemplo para simular transferencias bancarias. Se provee una API sencilla, un frontend básico y tareas asíncronas con Celery.

## Instalación rápida

```bash
python -m venv venv
source venv/bin/activate
pip install -r simulador_banco/requirements.txt
cp simulador_banco/.env.example simulador_banco/.env
python simulador_banco/manage.py migrate
python simulador_banco/manage.py runserver
```

Consulte `simulador_banco/README.md` para más información.
