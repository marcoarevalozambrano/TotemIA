# Despliegue de TotemIA v2.0 en GCP (Debian 12)

> IP compartida con otros servicios · Dominio temporal gratuito · SSL con Let's Encrypt  
> Stack: Nginx (reverse proxy) + Gunicorn + Django + MariaDB (Docker)

---

## 0. Diagnóstico previo de la VM

Ejecutar estos comandos en la VM y compartir la salida para evaluar el estado actual:

```bash
echo "===== SISTEMA ====="
uname -a
cat /etc/debian_version

echo ""
echo "===== IP PÚBLICA ====="
curl -s ifconfig.me

echo ""
echo "===== PUERTOS EN USO ====="
sudo ss -tlnp

echo ""
echo "===== DOCKER ====="
docker --version 2>/dev/null || echo "NO INSTALADO"
docker compose version 2>/dev/null || echo "NO INSTALADO"
docker ps -a 2>/dev/null || echo "NO ACCESIBLE"

echo ""
echo "===== NGINX ====="
nginx -v 2>&1 || echo "NO INSTALADO"
sudo systemctl is-active nginx 2>/dev/null || echo "NO ACTIVO"
ls /etc/nginx/sites-enabled/ 2>/dev/null || echo "SIN SITES"

echo ""
echo "===== PYTHON ====="
python3 --version 2>/dev/null || echo "NO INSTALADO"
pip3 --version 2>/dev/null || echo "NO INSTALADO"

echo ""
echo "===== GIT ====="
git --version 2>/dev/null || echo "NO INSTALADO"

echo ""
echo "===== CERTBOT ====="
certbot --version 2>/dev/null || echo "NO INSTALADO"

echo ""
echo "===== LIBMARIADB-DEV (necesario para mysqlclient) ====="
dpkg -l | grep libmariadb-dev 2>/dev/null || echo "NO INSTALADO"

echo ""
echo "===== BUILD TOOLS ====="
gcc --version 2>/dev/null | head -1 || echo "gcc NO INSTALADO"
pkg-config --version 2>/dev/null || echo "pkg-config NO INSTALADO"

echo ""
echo "===== DISCO ====="
df -h /

echo ""
echo "===== MEMORIA ====="
free -h

echo ""
echo "===== FIREWALL GCP (reglas locales) ====="
sudo iptables -L -n 2>/dev/null | head -20 || echo "NO ACCESIBLE"
```

### Resultado del diagnóstico

| Componente | Estado | Acción |
|------------|--------|--------|
| Debian 12 (6.1.0-41-cloud-amd64) | ✅ OK | — |
| IP pública: `34.172.84.111` | ✅ OK | — |
| Nginx (activo, puertos 80/443) | ✅ Instalado | Solo agregar server block |
| Sites existentes: `default`, `klinexia`, `pet24`, `pet24real` | ✅ OK | No tocar |
| Python 3.11.2 | ✅ Instalado | — |
| pip 23.0.1 | ✅ Instalado | — |
| Git 2.39.5 | ✅ Instalado | — |
| Certbot 2.1.0 | ✅ Instalado | — |
| gcc 12.2.0 | ✅ Instalado | — |
| pkg-config 1.8.1 | ✅ Instalado | — |
| Docker | ❌ No instalado | **Instalar** |
| libmariadb-dev | ❌ No instalado | **Instalar** |
| Disco: 40GB libres | ✅ OK | — |
| RAM: 3.8GB (2.6GB disponible) | ✅ OK | — |
| Firewall: ACCEPT all | ✅ OK | Verificar reglas GCP |

---

## 1. Datos de este despliegue

| Dato | Valor |
|------|-------|
| IP pública de la VM | `34.172.84.111` |
| Puerto interno Gunicorn | `8000` (solo localhost) |
| Puerto MariaDB Docker | `3306` (solo localhost) |
| Dominio temporal | `totem-ia.duckdns.org` (o el que elijas) |
| Repo | `https://github.com/marcoarevalozambrano/TotemIA.git` rama `v2.0-mariadb` |

---

## 2. Obtener dominio temporal gratuito (DuckDNS)

1. Ir a [https://www.duckdns.org](https://www.duckdns.org)
2. Iniciar sesión con Google/GitHub/etc.
3. Crear un subdominio, por ejemplo: `totem-ia` → te queda `totem-ia.duckdns.org`
4. Apuntar el dominio a `34.172.84.111`
5. Anotar el **token** que te da DuckDNS

### Actualizar DNS automáticamente (cron)

```bash
mkdir -p ~/duckdns
cat > ~/duckdns/duck.sh << 'EOF'
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=TU_SUBDOMINIO&token=TU_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -
EOF

# Reemplazar TU_SUBDOMINIO y TU_TOKEN con tus datos reales
nano ~/duckdns/duck.sh

chmod 700 ~/duckdns/duck.sh

# Probar
~/duckdns/duck.sh
cat ~/duckdns/duck.log
# Debe decir "OK"

# Cron cada 5 minutos
(crontab -l 2>/dev/null; echo "*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1") | crontab -
```

---

## 3. Instalar lo que falta

### 3.1 libmariadb-dev (para compilar mysqlclient de Python)

```bash
sudo apt update
sudo apt install -y libmariadb-dev python3-dev
```

### 3.2 Docker

```bash
# Dependencias
sudo apt install -y ca-certificates curl gnupg

# Clave GPG de Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Usar docker sin sudo
sudo usermod -aG docker $USER
newgrp docker

# Verificar
docker --version
docker compose version
```

---

## 4. Levantar MariaDB en Docker

```bash
# Directorio para datos persistentes
sudo mkdir -p /opt/mariadb_data

# Levantar contenedor
docker run -d \
  --name mariadb-totem \
  --restart always \
  -e MYSQL_ROOT_PASSWORD=ROOT_PASSWORD_SEGURA \
  -e MYSQL_DATABASE=totem_ia \
  -e MYSQL_USER=totem \
  -e MYSQL_PASSWORD=TU_PASSWORD_SEGURA \
  -e MYSQL_CHARACTER_SET_SERVER=utf8mb4 \
  -e MYSQL_COLLATION_SERVER=utf8mb4_unicode_ci \
  -v /opt/mariadb_data:/var/lib/mysql \
  -p 127.0.0.1:3306:3306 \
  mariadb:11
```

> El bind a `127.0.0.1:3306` asegura que MariaDB no queda expuesto a internet.

### Verificar

```bash
docker ps
docker logs mariadb-totem

# Probar conexión (esperar ~10 seg a que inicie)
docker exec -it mariadb-totem mariadb -u totem -p totem_ia -e "SELECT 1;"
```

### Comandos útiles del contenedor

```bash
# Logs
docker logs -f mariadb-totem

# Reiniciar
docker restart mariadb-totem

# Consola SQL
docker exec -it mariadb-totem mariadb -u root -p

# Backup
docker exec mariadb-totem mariadb-dump -u root -pROOT_PASSWORD_SEGURA totem_ia > ~/backup_totem_$(date +%Y%m%d).sql

# Restaurar
docker exec -i mariadb-totem mariadb -u root -pROOT_PASSWORD_SEGURA totem_ia < ~/backup.sql
```

---

## 5. Desplegar la aplicación

### 5.1 Clonar el proyecto

```bash
cd /opt
sudo mkdir -p totem_ia
sudo chown $USER:$USER totem_ia
git clone -b v2.0-mariadb https://github.com/marcoarevalozambrano/TotemIA.git totem_ia
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
SECRET_KEY=GENERA_UNA_CLAVE_AQUI
EOF

chmod 600 /opt/totem_ia/.env
```

Generar la SECRET_KEY:

```bash
/opt/totem_ia/venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar el resultado y pegarlo en el `.env` como valor de `SECRET_KEY`.

### 5.4 Ajustar settings.py para producción

Editar `totem_ia/settings.py`:

```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-solo-desarrollo')
DEBUG = False
ALLOWED_HOSTS = ['totem-ia.duckdns.org', '34.172.84.111']

CSRF_TRUSTED_ORIGINS = [
    'https://totem-ia.duckdns.org',
]

# Agregar para producción (collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### 5.5 Migraciones y archivos estáticos

```bash
cd /opt/totem_ia
source venv/bin/activate
export $(grep -v '^#' .env | xargs)

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 6. Configurar Gunicorn como servicio systemd

```bash
sudo tee /etc/systemd/system/totem_ia.service > /dev/null << 'EOF'
[Unit]
Description=TotemIA Gunicorn Daemon
After=network.target docker.service
Requires=docker.service

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
sudo mkdir -p /var/log/totem_ia
sudo chown www-data:www-data /var/log/totem_ia
sudo chown -R www-data:www-data /opt/totem_ia

sudo systemctl daemon-reload
sudo systemctl enable totem_ia
sudo systemctl start totem_ia
sudo systemctl status totem_ia
```

---

## 7. Agregar server block en Nginx

Tu Nginx ya tiene: `default`, `klinexia`, `pet24`, `pet24real`. Solo agregamos uno más.

```bash
sudo tee /etc/nginx/sites-available/totem_ia > /dev/null << 'NGINX'
server {
    listen 80;
    server_name totem-ia.duckdns.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /opt/totem_ia/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /opt/totem_ia/media/;
        expires 7d;
    }

    client_max_body_size 10M;
}
NGINX
```

```bash
# Activar el sitio
sudo ln -sf /etc/nginx/sites-available/totem_ia /etc/nginx/sites-enabled/

# Verificar que no rompa los otros sites
sudo nginx -t

# Recargar (sin reiniciar, no afecta los otros servicios)
sudo systemctl reload nginx
```

---

## 8. Verificar puertos en firewall GCP

Tus puertos 80 y 443 ya están abiertos (Nginx ya escucha ahí para los otros sites).  
Solo verificar que las reglas de firewall de GCP permitan tráfico entrante en 80 y 443.

En la consola GCP → VPC Network → Firewall Rules, buscar reglas que incluyan tcp:80 y tcp:443.  
Si no existen:

```bash
gcloud compute firewall-rules create allow-http-https \
  --allow tcp:80,tcp:443 \
  --source-ranges 0.0.0.0/0 \
  --description "Permitir HTTP y HTTPS"
```

---

## 9. Obtener certificado SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d totem-ia.duckdns.org

# Seguir instrucciones:
# - Email
# - Aceptar términos
# - Redirigir HTTP a HTTPS (recomendado)
```

Certbot modifica automáticamente el server block de Nginx para agregar SSL.

### Renovación automática

```bash
# Ya deberías tener el timer activo (certbot ya está instalado)
sudo systemctl status certbot.timer

# Si no está activo:
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Probar
sudo certbot renew --dry-run
```

---

## 10. Verificación final

```bash
# MariaDB en Docker
docker ps | grep mariadb-totem

# Gunicorn
sudo systemctl status totem_ia

# Nginx
sudo systemctl status nginx

# Test local
curl -I http://127.0.0.1:8000/

# Test público
curl -I https://totem-ia.duckdns.org/
```

| Interfaz | URL |
|----------|-----|
| Totem | `https://totem-ia.duckdns.org/` |
| Pantalla | `https://totem-ia.duckdns.org/pantalla/` |
| Mesa | `https://totem-ia.duckdns.org/mesa/` |
| Admin | `https://totem-ia.duckdns.org/admin-panel/` |

---

## 11. Comandos de mantenimiento

```bash
# --- Logs ---
sudo journalctl -u totem_ia -f
sudo tail -f /var/log/totem_ia/error.log
docker logs -f mariadb-totem

# --- Reiniciar servicios ---
sudo systemctl restart totem_ia
sudo nginx -t && sudo systemctl reload nginx
docker restart mariadb-totem

# --- Actualizar código ---
cd /opt/totem_ia
sudo -u www-data git pull
sudo -u www-data /opt/totem_ia/venv/bin/python manage.py migrate
sudo -u www-data /opt/totem_ia/venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart totem_ia

# --- Backup de BD ---
docker exec mariadb-totem mariadb-dump -u root -pROOT_PASSWORD_SEGURA totem_ia > ~/backup_totem_$(date +%Y%m%d).sql

# --- Restaurar BD ---
docker exec -i mariadb-totem mariadb -u root -pROOT_PASSWORD_SEGURA totem_ia < ~/backup.sql
```

---

## Arquitectura final

```
Internet
   │
   ▼
[GCP Firewall: 80, 443]
   │
   ▼
[Nginx :80/:443]  ← SSL (Let's Encrypt)
   │  ├── klinexia        (site existente)
   │  ├── pet24           (site existente)
   │  ├── pet24real       (site existente)
   │  └── totem-ia.duckdns.org → proxy_pass
   │        ├── /static/  → /opt/totem_ia/staticfiles/
   │        ├── /media/   → /opt/totem_ia/media/
   │        └── /*        → 127.0.0.1:8000
   ▼
[Gunicorn :8000]  ← 3 workers, solo localhost
   │
   ▼
[Django - TotemIA]
   │
   ▼
[Docker: MariaDB :3306]  ← solo localhost, datos en /opt/mariadb_data
```

---

## Notas importantes

- **IP compartida**: Nginx separa por `server_name`. Tu TotemIA convive con klinexia, pet24 y pet24real sin conflicto.
- **Seguridad**: Gunicorn (`127.0.0.1:8000`) y MariaDB Docker (`127.0.0.1:3306`) no están expuestos a internet.
- **Persistencia**: Datos de MariaDB en `/opt/mariadb_data`. Si el contenedor se destruye, los datos se mantienen.
- **Auto-restart**: El contenedor Docker tiene `--restart always` y Gunicorn tiene `Restart=always` en systemd. Ambos se levantan solos al reiniciar la VM.
- **DuckDNS**: Dominio gratuito e indefinido. Si después necesitas un dominio real, solo cambias `server_name` en Nginx y regeneras el certificado.
