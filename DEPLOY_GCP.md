# Despliegue de TotemIA v2.0 en GCP (Debian 12)

> IP compartida con otros servicios · Dominio temporal gratuito · SSL con Let's Encrypt  
> Stack: Nginx (reverse proxy) + Gunicorn + Django + MariaDB

---

## 1. Datos previos que necesitas tener

| Dato | Ejemplo | Notas |
|------|---------|-------|
| IP pública de la VM | `34.xx.xx.xx` | La obtienes de la consola GCP |
| Puerto libre para la app | `8000` (interno) | Gunicorn escuchará aquí, Nginx hace proxy |
| Dominio temporal | `totem-ia.duckdns.org` | Lo crearemos en el paso 2 |
| Token DuckDNS | (se genera al registrarse) | Para actualizar el DNS |

---

## 2. Obtener dominio temporal gratuito (DuckDNS)

DuckDNS es gratuito, no requiere tarjeta, y funciona perfecto para esto.

1. Ir a [https://www.duckdns.org](https://www.duckdns.org)
2. Iniciar sesión con Google/GitHub/etc.
3. Crear un subdominio, por ejemplo: `totem-ia` → te queda `totem-ia.duckdns.org`
4. Apuntar el dominio a tu IP pública de GCP
5. Anotar el **token** que te da DuckDNS (lo necesitarás)

### Actualizar DNS automáticamente (cron)

```bash
# Crear script de actualización
mkdir -p ~/duckdns
cat > ~/duckdns/duck.sh << 'EOF'
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=TU_SUBDOMINIO&token=TU_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -
EOF

# Reemplazar TU_SUBDOMINIO y TU_TOKEN con tus datos reales
nano ~/duckdns/duck.sh

chmod 700 ~/duckdns/duck.sh

# Probar que funcione
./duckdns/duck.sh
cat ~/duckdns/duck.log
# Debe decir "OK"

# Agregar al cron (cada 5 minutos)
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1") | crontab -
```

---

## 3. Preparar la VM (paquetes base)

```bash
sudo apt update && sudo apt upgrade -y

# Paquetes esenciales
sudo apt install -y \
  python3 python3-pip python3-venv \
  nginx \
  mariadb-server \
  certbot python3-certbot-nginx \
  git \
  libmariadb-dev \
  pkg-config \
  build-essential \
  python3-dev
```

---

## 4. Configurar MariaDB

```bash
# Asegurar la instalación
sudo mysql_secure_installation
# Responder: Y a todo, definir contraseña de root

# Crear base de datos y usuario
sudo mysql -u root -p
```

```sql
CREATE DATABASE totem_ia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'totem'@'localhost' IDENTIFIED BY 'TU_PASSWORD_SEGURA';
GRANT ALL PRIVILEGES ON totem_ia.* TO 'totem'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## 5. Desplegar la aplicación

### 5.1 Clonar o subir el proyecto

```bash
# Opción A: Si tienes el repo en Git
cd /opt
sudo mkdir totem_ia
sudo chown $USER:$USER totem_ia
git clone TU_REPO_URL totem_ia

# Opción B: Subir con scp desde tu máquina local
# (desde tu PC)
# scp -r ./totem_ia usuario@IP_VM:/opt/totem_ia
```

### 5.2 Entorno virtual y dependencias

```bash
cd /opt/totem_ia
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 5.3 Configurar variables de entorno

```bash
cat > /opt/totem_ia/.env << 'EOF'
DB_ENGINE=mariadb
DB_NAME=totem_ia
DB_USER=totem
DB_PASSWORD=TU_PASSWORD_SEGURA
DB_HOST=127.0.0.1
DB_PORT=3306
EOF

chmod 600 /opt/totem_ia/.env
```

### 5.4 Ajustar settings.py para producción

Editar `totem_ia/settings.py` y cambiar:

```python
DEBUG = False
ALLOWED_HOSTS = ['totem-ia.duckdns.org', 'TU_IP_PUBLICA']

# Agregar a CSRF_TRUSTED_ORIGINS:
CSRF_TRUSTED_ORIGINS = [
    'https://totem-ia.duckdns.org',
    # ... mantener los existentes si los necesitas
]

# Archivos estáticos para producción
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 5.5 Migraciones y archivos estáticos

```bash
cd /opt/totem_ia
source venv/bin/activate

# Cargar variables de entorno
export $(grep -v '^#' .env | xargs)

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 6. Configurar Gunicorn como servicio systemd

```bash
sudo cat > /etc/systemd/system/totem_ia.service << 'EOF'
[Unit]
Description=TotemIA Gunicorn Daemon
After=network.target mariadb.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/totem_ia
EnvironmentFile=/opt/totem_ia/.env
ExecStart=/opt/totem_ia/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/log/totem_ia/access.log \
    --error-logfile /var/log/totem_ia/error.log \
    totem_ia.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
```

```bash
# Crear directorio de logs y ajustar permisos
sudo mkdir -p /var/log/totem_ia
sudo chown www-data:www-data /var/log/totem_ia

# Dar permisos a www-data sobre el proyecto
sudo chown -R www-data:www-data /opt/totem_ia

# Habilitar e iniciar el servicio
sudo systemctl daemon-reload
sudo systemctl enable totem_ia
sudo systemctl start totem_ia
sudo systemctl status totem_ia
```

---

## 7. Configurar Nginx como reverse proxy

Como la IP es compartida con otros servicios, usamos un server block separado por dominio.

```bash
sudo cat > /etc/nginx/sites-available/totem_ia << 'NGINX'
server {
    listen 80;
    server_name totem-ia.duckdns.org;

    # Redirigir todo HTTP a HTTPS (se activa después de obtener SSL)
    # return 301 https://$host$request_uri;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Archivos estáticos (servidos directamente por Nginx)
    location /static/ {
        alias /opt/totem_ia/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Archivos media (uploads)
    location /media/ {
        alias /opt/totem_ia/media/;
        expires 7d;
    }

    # Limitar tamaño de uploads
    client_max_body_size 10M;
}
NGINX
```

```bash
# Activar el sitio
sudo ln -s /etc/nginx/sites-available/totem_ia /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx
```

---

## 8. Abrir puertos en el firewall de GCP

En la consola de GCP → VPC Network → Firewall Rules:

1. Verificar que exista una regla que permita tráfico TCP en puertos **80** y **443** hacia tu VM
2. Si no existe, crear una regla:
   - Nombre: `allow-http-https`
   - Dirección: Ingress
   - Destinos: Todas las instancias (o la etiqueta de tu VM)
   - Rangos de IP de origen: `0.0.0.0/0`
   - Protocolos y puertos: TCP `80, 443`

También puedes hacerlo por CLI:

```bash
# Desde tu máquina local con gcloud instalado, o desde Cloud Shell
gcloud compute firewall-rules create allow-http-https \
  --allow tcp:80,tcp:443 \
  --source-ranges 0.0.0.0/0 \
  --description "Permitir HTTP y HTTPS"
```

---

## 9. Obtener certificado SSL gratuito (Let's Encrypt)

```bash
# Certbot con plugin de Nginx (automático)
sudo certbot --nginx -d totem-ia.duckdns.org

# Seguir las instrucciones:
# - Ingresar email
# - Aceptar términos
# - Elegir redirigir HTTP a HTTPS (opción 2, recomendado)
```

Certbot modificará automáticamente tu config de Nginx para agregar SSL.

### Renovación automática

```bash
# Verificar que el timer de renovación esté activo
sudo systemctl status certbot.timer

# Si no está activo:
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Probar renovación (dry-run)
sudo certbot renew --dry-run
```

---

## 10. Verificación final

```bash
# 1. Verificar que Gunicorn esté corriendo
sudo systemctl status totem_ia

# 2. Verificar que Nginx esté corriendo
sudo systemctl status nginx

# 3. Probar localmente
curl -I http://127.0.0.1:8000/

# 4. Probar desde el dominio
curl -I https://totem-ia.duckdns.org/
```

Acceder desde el navegador:
- Totem: `https://totem-ia.duckdns.org/`
- Pantalla: `https://totem-ia.duckdns.org/pantalla/`
- Mesa: `https://totem-ia.duckdns.org/mesa/`
- Admin: `https://totem-ia.duckdns.org/admin-panel/`

---

## 11. Comandos útiles de mantenimiento

```bash
# Ver logs de la aplicación
sudo journalctl -u totem_ia -f
sudo tail -f /var/log/totem_ia/error.log

# Reiniciar después de cambios en el código
sudo systemctl restart totem_ia

# Reiniciar Nginx después de cambios en config
sudo nginx -t && sudo systemctl reload nginx

# Actualizar código (si usas git)
cd /opt/totem_ia
sudo -u www-data git pull
sudo -u www-data /opt/totem_ia/venv/bin/python manage.py migrate
sudo -u www-data /opt/totem_ia/venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart totem_ia
```

---

## Resumen de la arquitectura

```
Internet
   │
   ▼
[GCP Firewall: 80, 443]
   │
   ▼
[Nginx :80/:443]  ← SSL (Let's Encrypt)
   │                  ├── /static/  → /opt/totem_ia/staticfiles/
   │                  ├── /media/   → /opt/totem_ia/media/
   │                  └── /*        → proxy_pass
   ▼
[Gunicorn :8000]  ← 3 workers, solo localhost
   │
   ▼
[Django - TotemIA]
   │
   ▼
[MariaDB :3306]   ← solo localhost
```

---

## Notas importantes

- **IP compartida**: Nginx separa los servicios por `server_name` (dominio). Cada servicio en la VM tiene su propio server block. No hay conflicto.
- **Seguridad**: Gunicorn y MariaDB solo escuchan en `127.0.0.1`. Solo Nginx está expuesto.
- **DuckDNS**: El dominio es gratuito e indefinido. Si necesitas algo más profesional después, puedes apuntar un dominio real y solo cambiar el `server_name` en Nginx + regenerar el certificado.
- **SECRET_KEY**: Para producción, genera una nueva clave secreta y ponla en el `.env`:
  ```bash
  python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Y en `settings.py`: `SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-inseguro')`
