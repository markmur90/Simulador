# Simulador Bancario

Este proyecto es un ejemplo mínimo de un simulador de transferencias bancarias usando Django.

## Instalación

1. Crear un entorno virtual e instalar dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r simulador_banco/requirements.txt
   ```
2. Copiar el archivo `.env.example` a `.env` y ajustar los valores de las variables.
   El `FIELD_ENCRYPTION_KEY` puede generarse con:
   ```python
   from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())
   ```
3. Ejecutar migraciones:
   ```bash
   export FIELD_ENCRYPTION_KEY=<clave>
   python simulador_banco/manage.py migrate
   ```
4. Crear un superusuario para acceder al admin:
   ```bash
   python simulador_banco/manage.py createsuperuser
   ```
5. Iniciar el servidor de desarrollo:
   ```bash
   python simulador_banco/manage.py runserver
   ```

## Notas

- Las claves secretas y valores sensibles deben definirse en el archivo `.env`.
- Para un entorno seguro, configure `DEBUG=0` y agregue los dominios válidos en `ALLOWED_HOSTS`.
