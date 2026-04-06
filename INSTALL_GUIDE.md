# Guía de Instalación — TotemIA v2.0 en VM GCP

> Debian 12 · IP: 34.172.84.111 · Fecha base: Abril 2026  
> Esta guía es secuencial. Ejecutar cada paso en orden.

---

## PASO 1 — Actualizar el sistema

```bash
sudo apt update && sudo apt upgrade -y
```

---

## PASO 2 — Instalar libmariadb-dev y python3-dev

Necesarios para compilar el paquete `mysqlclient` de Python.

```bash
sudo apt install -y libmariadb-dev python3-dev
```

Verificar:

```bash
dpkg -l | grep libmariadb-dev
# Debe mostrar una línea con "ii  libmariadb-dev ..."
```

---

## PASO 3 — Instalar Docker

### 3.1 Dependencias previas

```bash
sudo apt install -y ca-certificates curl gnupg
```

### 3.2 Agregar clave GPG y repositorio de Docker

```bash
sudo install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/debian/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 3.3 Instalar Docker Engine

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 3.4 Permitir usar Docker sin sudo

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 3.5 Verificar

```bash
docker --version
# Docker version 2x.x.x

docker compose version
# Docker Compose version v2.x.x

docker run --rm hello-world
# Debe imprimir "Hello from Docker!"
```

---

## PASO 4 — Levantar MariaDB en Docker

### 4.1 Crear directorio de datos persistentes

```bash
sudo mkdir -p /opt/mariadb_data
```

### 4.2 Levantar el contenedor

> ⚠️ Reemplazar `ROOT_PASSWORD_SEGURA` y `TU_PASSWORD_SEGURA` con contraseñas reales.

```bash
docker run -d \
  --name mariadb-totem \
  --restart always \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=totem_ia \
  -e MYSQL_USER=totem \
  -e MYSQL_PASSWORD=Inacap2026 \
  -e MYSQL_CHARACTER_SET_SERVER=utf8mb4 \
  -e MYSQL_COLLATION_SERVER=utf8mb4_unicode_ci \
  -v /opt/mariadb_data:/var/lib/mysql \
  -p 127.0.0.1:3306:3306 \
  mariadb:11
```

### 4.3 Verificar que esté corriendo

```bash
# Esperar ~15 segundos a que inicie completamente
sleep 15

docker ps
# Debe mostrar mariadb-totem con STATUS "Up"

docker logs mariadb-totem | tail -5
# Debe terminar con algo como "ready for connections"
```

### 4.4 Probar conexión

```bash
docker exec -it mariadb-totem mariadb -u totem -pInacap2026 totem_ia -e "SELECT 1 AS test;"
# Debe devolver:
# +------+
# | test |
# +------+
# |    1 |
# +------+
```

### 4.5 Verificar que solo escucha en localhost

```bash
sudo ss -tlnp | grep 3306
# Debe mostrar 127.0.0.1:3306 (NO 0.0.0.0:3306)
```

---

## PASO 5 — Clonar el proyecto

```bash
cd /opt
sudo mkdir -p totem_ia
sudo chown $USER:$USER totem_ia

git clone -b v2.0-mariadb https://github.com/marcoarevalozambrano/TotemIA.git totem_ia
```

Verificar:

```bash
ls /opt/totem_ia/manage.py
# Debe existir
```

---

## PASO 6 — Crear entorno virtual e instalar dependencias

```bash
cd /opt/totem_ia

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

Verificar:

```bash
pip list | grep -E "Django|gunicorn|mysqlclient"
# Debe mostrar los tres paquetes instalados
```

---

## PASO 7 — Configurar variables de entorno

> ⚠️ Usar la misma contraseña que pusiste en el PASO 4 para `DB_PASSWORD`.

```bash
cat > /opt/totem_ia/.env << 'EOF'
DB_ENGINE=mariadb
DB_NAME=totem_ia
DB_USER=totem
DB_PASSWORD=TU_PASSWORD_SEGURA
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=PEGAR_CLAVE_AQUI
EOF

chmod 600 /opt/totem_ia/.env
```

### Generar SECRET_KEY

```bash
/opt/totem_ia/venv/bin/python -c \
  "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiar la salida y reemplazar `PEGAR_CLAVE_AQUI` en el `.env`:

```bash
nano /opt/totem_ia/.env
```

---

## PASO 8 — Ajustar settings.py para producción

```bash
nano /opt/totem_ia/totem_ia/settings.py
```

Cambios a realizar:

1. **SECRET_KEY** — reemplazar la línea hardcodeada:
```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-solo-desarrollo')
```

2. **DEBUG** — desactivar:
```python
DEBUG = False
```

3. **ALLOWED_HOSTS** — poner tu dominio e IP:
```python
ALLOWED_HOSTS = ['totem-ia.duckdns.org', '34.172.84.111']
```

4. **CSRF_TRUSTED_ORIGINS** — agregar tu dominio:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://totem-ia.duckdns.org',
]
```

5. **STATIC_ROOT** — agregar al final de la sección de estáticos:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Guardar y salir (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

## PASO 9 — Ejecutar migraciones y collectstatic

```bash
cd /opt/totem_ia
source venv/bin/activate
export $(grep -v '^#' .env | xargs)

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
# Ingresar usuario, email y contraseña del admin
```

Verificar:

```bash
# Debe existir el directorio de estáticos recopilados
ls /opt/totem_ia/staticfiles/
# Debe tener contenido

# Probar que Django arranca sin errores
python manage.py check --deploy
# Puede mostrar warnings (normal), pero no errores críticos
```

---

## PASO 10 — Configurar Gunicorn como servicio systemd

### 10.1 Crear el archivo de servicio

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

### 10.2 Preparar permisos y directorios

```bash
sudo mkdir -p /var/log/totem_ia
sudo chown www-data:www-data /var/log/totem_ia
sudo chown -R www-data:www-data /opt/totem_ia
```

### 10.3 Habilitar e iniciar

```bash
sudo systemctl daemon-reload
sudo systemctl enable totem_ia
sudo systemctl start totem_ia
```

### 10.4 Verificar

```bash
sudo systemctl status totem_ia
# Debe decir "active (running)"

curl -I http://127.0.0.1:8000/
# Debe responder HTTP (200 o 302)

# Si hay errores:
sudo journalctl -u totem_ia --no-pager -n 30
sudo tail -20 /var/log/totem_ia/error.log
```

---

## PASO 11 — Agregar server block en Nginx

### 11.1 Crear configuración

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

### 11.2 Activar y verificar

```bash
sudo ln -sf /etc/nginx/sites-available/totem_ia /etc/nginx/sites-enabled/

# IMPORTANTE: verificar que no rompa los otros sites
sudo nginx -t
# Debe decir "syntax is ok" y "test is successful"

# Recargar (no reiniciar, para no afectar klinexia/pet24/pet24real)
sudo systemctl reload nginx
```

### 11.3 Verificar que los otros sites siguen funcionando

```bash
ls /etc/nginx/sites-enabled/
# Debe mostrar: default  klinexia  pet24  pet24real  totem_ia
```

---

## PASO 12 — Configurar DuckDNS

> Si aún no lo hiciste en el PASO 2 de DEPLOY_GCP.md, hacerlo ahora.

Verificar que el dominio resuelve a tu IP:

```bash
dig +short totem-ia.duckdns.org
# Debe devolver: 34.172.84.111

# O con curl
curl -s http://totem-ia.duckdns.org/ -o /dev/null -w "%{http_code}"
# Debe devolver 200 o 302
```

---

## PASO 13 — Obtener certificado SSL con Certbot

```bash
sudo certbot --nginx -d totem-ia.duckdns.org
```

Seguir las instrucciones:
1. Ingresar email
2. Aceptar términos (Y)
3. Compartir email con EFF (opcional, N)
4. Redirigir HTTP a HTTPS → elegir **sí** (recomendado)

### Verificar renovación automática

```bash
sudo systemctl status certbot.timer
# Debe estar active

sudo certbot renew --dry-run
# Debe terminar sin errores
```

---

## PASO 14 — Verificación final completa

Ejecutar todo este bloque y compartir la salida:

```bash
echo "===== DOCKER: MariaDB ====="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep mariadb

echo ""
echo "===== GUNICORN ====="
sudo systemctl is-active totem_ia

echo ""
echo "===== NGINX ====="
sudo systemctl is-active nginx
sudo nginx -t 2>&1

echo ""
echo "===== SSL ====="
sudo certbot certificates 2>/dev/null | grep -A3 "totem-ia"

echo ""
echo "===== TEST LOCAL ====="
curl -s -o /dev/null -w "HTTP %{http_code}" http://127.0.0.1:8000/

echo ""
echo "===== TEST PÚBLICO ====="
curl -s -o /dev/null -w "HTTPS %{http_code}" https://totem-ia.duckdns.org/

echo ""
echo "===== PUERTOS ====="
sudo ss -tlnp | grep -E ':(80|443|3306|8000)\s'
```

Resultado esperado:

```
===== DOCKER: MariaDB =====
mariadb-totem   Up X minutes   127.0.0.1:3306->3306/tcp

===== GUNICORN =====
active

===== NGINX =====
active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

===== SSL =====
  Certificate Name: totem-ia.duckdns.org
    Domains: totem-ia.duckdns.org
    Expiry Date: 20XX-XX-XX

===== TEST LOCAL =====
HTTP 200 o 302

===== TEST PÚBLICO =====
HTTPS 200 o 302

===== PUERTOS =====
... :80 ... nginx
... :443 ... nginx
... 127.0.0.1:3306 ... docker
... 127.0.0.1:8000 ... gunicorn
```

---

## Troubleshooting rápido

| Problema | Comando de diagnóstico | Solución común |
|----------|----------------------|----------------|
| Gunicorn no arranca | `sudo journalctl -u totem_ia -n 50` | Revisar `.env`, permisos, o error en settings.py |
| Error 502 en Nginx | `curl http://127.0.0.1:8000/` | Gunicorn no está corriendo, reiniciar servicio |
| Error de BD | `docker logs mariadb-totem` | Contenedor caído, `docker start mariadb-totem` |
| Certbot falla | `sudo certbot --nginx -d dominio --dry-run` | DNS no resuelve aún, esperar propagación |
| Static files 404 | `ls /opt/totem_ia/staticfiles/` | Ejecutar `collectstatic` de nuevo |
| Permiso denegado | `ls -la /opt/totem_ia/` | `sudo chown -R www-data:www-data /opt/totem_ia` |
| mysqlclient no compila | `dpkg -l \| grep libmariadb-dev` | `sudo apt install libmariadb-dev python3-dev` |
