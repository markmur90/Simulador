# Simulador Bancario

Este repositorio contiene un proyecto Django minimalista que funciona como simulador de transferencias bancarias. Se incluyen servicios básicos de autenticación mediante JWT y operaciones de transferencia, además de un pequeño frontend de pruebas.

## Instalación rápida

1. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r simulador_banco/requirements.txt
   ```
2. Copiar `.env.example` a `.env` y rellenar las variables requeridas:
   ```bash
   cp simulador_banco/.env.example simulador_banco/.env
   ```
   Las claves secretas **no** deben almacenarse en el repositorio.
3. Ejecutar migraciones y crear un superusuario:
   ```bash
   python simulador_banco/manage.py migrate
   python simulador_banco/manage.py createsuperuser
   ```
4. Iniciar el servidor de desarrollo:
   ```bash
   python simulador_banco/manage.py runserver
   ```

## Endpoint de transferencias entrantes

El proyecto expone `/api/transferencias/entrantes/` para recibir transferencias de sistemas externos. Es necesario autenticarse con JWT (ver `/api/token`). El cuerpo de la solicitud debe ser JSON y es procesado por `TransferService`.

## Pruebas manuales

- **Login**: acceder a `/` y autenticar con el superusuario creado.
- **Frontend de transferencia**: `/frontend/transfer` permite probar la obtención de token y el envío de transferencias.

Para un despliegue seguro revise la documentación existente en `docs/`.
