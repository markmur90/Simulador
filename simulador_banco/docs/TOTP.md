# Problema

Necesitamos obtener y exportar dos variables de entorno:

1. OPENAI_API_KEY: la clave secreta de la API de OpenAI.

2. TOTP_SECRET: el secreto Base32 para generar tokens TOTP (2FA).

## Implementación

———————— OPENAI_API_KEY ————————

1. Ve a tu cuenta de OpenAI: https://platform.openai.com/account/api-keys  

2. Haz clic en “Create new secret key” y copia el valor que empieza por “sk-…”.  

3. Exporta la variable en tu shell o en tu .env:

        export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

---
———————— TOTP_SECRET ————————

Puedes generar un secreto Base32 con Python y la librería estándar:

Generamos 80 bits (10 bytes) y los codificamos en Base32, sin padding:

    TOTP_SECRET=$(python3 - << 'EOF'
    import secrets, base64
    print(base64.b32encode(secrets.token_bytes(10)).decode('utf-8').rstrip('='))
    EOF
    )

    export TOTP_SECRET="$TOTP_SECRET"

# Ejemplo de Uso

1. Añade estas líneas a tu ~/.bashrc o ~/.zshenv (o al .env de tu proyecto).

2. Recarga tu shell: source ~/.bashrc

3. Verifica que estén correctas:

        echo "OPENAI_API_KEY=$OPENAI_API_KEY"
        echo "TOTP_SECRET=$TOTP_SECRET"

# Entrega en pantalla la solución

    echo "Variables OPENAI_API_KEY y TOTP_SECRET configuradas correctamente."
