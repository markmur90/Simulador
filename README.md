# 🧭 Guía de Despliegue Seguro: Proyecto Banco

## 📁 Estructura del Proyecto

```
/var/www/banco/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── ...
├── requirements.txt
├── .env
└── config.py
```

---

## 1. ⚙️ NGINX – `/etc/nginx/sites-available/banco.conf`

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/banco/app/static/;
    }

    location /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
        default_type text/plain;
    }
}
```

**Crear symlink:**
```bash
sudo ln -s /etc/nginx/sites-available/banco.conf /etc/nginx/sites-enabled/
```

---

## 2. ⚙️ Supervisor – `/etc/supervisor/conf.d/banco.conf`

```ini
[program:banco]
command=/var/www/banco/venv/bin/gunicorn --workers 3 --bind unix:/var/www/banco/banco.sock app.__init__:app
directory=/var/www/banco/app
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/banco/banco_supervisor.log
environment=PATH="/var/www/banco/venv/bin",SECRET_KEY="tu-clave-secreta"
```

**Crear carpeta de logs:**
```bash
sudo mkdir -p /var/log/banco
```

---

## 3. ⚙️ Fail2Ban – `/etc/fail2ban/jail.local`

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5
backend = auto
usedns = warn
ignoreip = 127.0.0.1/8 your.vps.ip.address

[http-get-dos]
enabled = true
port = http,https
protocol = tcp
filter = http-get-dos
logpath = /var/log/nginx/access.log
maxretry = 300
findtime = 600
bantime = 600
action = iptables[name=HTTP, port=http, protocol=tcp]

[banco-auth]
enabled = true
port = http,https
filter = banco-auth
logpath = /var/log/banco/banco_supervisor.log
maxretry = 3
findtime = 60
bantime = 3600
```

---

## 4. ⚙️ Tor (Opcional) – `/etc/tor/torrc`

```conf
HiddenServiceDir /var/lib/tor/banco/
HiddenServicePort 80 127.0.0.1:80
```

Esto crea una dirección `.onion` que apunta al NGINX local.

---

## 5. 🔒 Certificado SSL con Certbot

```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

Certbot modificará automáticamente `banco.conf` para usar HTTPS.

---

## 6. 🧪 Script de Deploy (opcional) – `deploy.sh`

```bash
#!/bin/bash

cd /var/www/banco || exit

# Actualiza repositorio
git pull origin main

# Actualiza dependencias
source venv/bin/activate
pip install -r requirements.txt

# Reinicia servicios
sudo supervisorctl reread
sudo supervisorctl restart banco
sudo systemctl reload nginx
```

**Permisos de ejecución:**
```bash
chmod +x deploy.sh
```

---

## ✅ Recomendaciones Finales

- **Logs**: Monitorea `/var/log/banco` y `/var/log/fail2ban`
- **Firewall**: Bloquea puertos no utilizados
- **Backups**: Usa `duplicity` o `rsync` para copias diarias
- **Monitoreo**: Considerá Prometheus + Grafana o Uptime Kuma
- **SSL Auto-Renew**: Probá con `certbot renew --dry-run`
- **Gunicorn**: Instala dependencias con `pip install -r simulador_banco/requirements.txt`
  y desactiva la opción `reload` en `config/gunicorn.conf.py` para evitar reinicios
  continuos en producción
  