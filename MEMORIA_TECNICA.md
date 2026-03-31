# TotemIA — Memoria Técnica del Sistema

## Documento de Arquitectura, Diseño, Funcionamiento y Características

**Versión:** 1.0  
**Fecha:** Marzo 2026  
**Plataforma:** Django 5.x / Python 3.13 / SQLite  
**Autor del desarrollo:** Asistido por IA (Kiro)

---

## 1. DESCRIPCIÓN GENERAL

TotemIA es un sistema de gestión de turnos y atención al público diseñado para entornos presenciales (oficinas de atención, instituciones educativas, servicios públicos). El sistema permite el registro de clientes mediante lectura OCR de cédula de identidad chilena (MRZ), la asignación automática de turnos, la visualización en pantalla grande para llamado público, la atención desde mesas de operadores, y la notificación en tiempo real al cliente en su dispositivo móvil.

### 1.1 Objetivos del Sistema
- Automatizar el flujo de atención de público con registro digital.
- Reducir tiempos de espera mediante priorización preferencial (tercera edad).
- Proveer visibilidad en tiempo real del estado de la cola.
- Permitir notificación directa al cliente en su celular.
- Ofrecer una plataforma completamente autoadministrable sin intervención técnica.

---

## 2. ARQUITECTURA DEL SISTEMA

### 2.1 Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Backend | Django 5.x (Python 3.13) |
| Base de datos | SQLite 3 |
| Frontend | HTML5, CSS3, JavaScript ES6+ |
| UI Framework | MaterializeCSS 1.0 |
| OCR | Tesseract.js 5 (client-side) |
| Gráficos | Chart.js 4 |
| Video | YouTube IFrame API, Vimeo Player API |
| Servidor HTTPS | wsgiref + ssl (desarrollo) |
| Túnel público | zrok (opcional) |
| Exportación | openpyxl (Excel .xlsx) |
| Certificados | cryptography (Python) |

### 2.2 Estructura del Proyecto

```
TotemIA/
├── totem_ia/                  # Configuración Django
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # URLs raíz
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
├── core/                      # Aplicación principal
│   ├── models.py              # 10 modelos de datos
│   ├── views.py               # 20+ vistas y APIs
│   ├── urls.py                # Rutas de la aplicación
│   ├── admin.py               # Configuración Django Admin
│   └── migrations/            # Migraciones de BD
├── templates/
│   ├── base.html              # Template base con tema dinámico
│   └── core/
│       ├── totem.html          # Interfaz de registro (totem)
│       ├── turno_confirmado.html # Confirmación en celular
│       ├── pantalla.html       # Pantalla de llamado
│       ├── mesa.html           # Interfaz del operador
│       ├── admin_panel.html    # Panel de administración
│       ├── login.html          # Login
│       └── logs.html           # Visor de logs
├── static/
│   ├── belldoor.wav           # Audio de llamado
│   └── logos/                 # Logos estáticos
├── media/                     # Archivos subidos (logos dinámicos)
├── run_https.py               # Servidor HTTPS desarrollo
├── generate_cert.py           # Generador de certificados SSL
├── cargar_usuarios.py         # Script de carga masiva de usuarios
├── manage.py                  # CLI Django
└── db.sqlite3                 # Base de datos
```

### 2.3 Diagrama de Arquitectura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   TOTEM      │     │  PANTALLA    │     │  CELULAR        │
│   (/)        │     │  (/pantalla) │     │  (/turno-conf.) │
│              │     │              │     │                 │
│ Cámara+OCR   │     │ Polling 3s   │     │ Polling 3s      │
│ Registro     │     │ Audio+Video  │     │ Vibración       │
│ cliente      │     │ Logos+Marq.  │     │ Alertas         │
└──────┬───────┘     └──────┬───────┘     └────────┬────────┘
       │                    │                      │
       │         ┌──────────┴──────────┐           │
       └─────────┤   DJANGO BACKEND    ├───────────┘
                 │                     │
                 │  APIs REST (JSON)   │
                 │  SQLite             │
                 │  Auth + Sessions    │
                 └──────────┬──────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       ┌──────┴───────┐          ┌────────┴───────┐
       │  MESA         │          │  ADMIN PANEL   │
       │  (/mesa)      │          │  (/admin-panel)│
       │               │          │                │
       │  Llamar turno │          │  Estadísticas  │
       │  Rellamar     │          │  Excel export  │
       │  Completar    │          │  Logs          │
       │  Editar datos │          │  Gestión       │
       └───────────────┘          └────────────────┘
```

---

## 3. MODELO DE DATOS

### 3.1 Modelos Principales

#### Mesa
Punto de atención físico donde un operador atiende clientes.

| Campo | Tipo | Descripción |
|---|---|---|
| nombre | CharField(50) | Nombre identificador (ej: "Mesa 1") |
| activa | BooleanField | Si la mesa está habilitada |
| preferencial | BooleanField | Si prioriza tercera edad |
| edad_preferencial | IntegerField | Edad mínima para prioridad (default: 60) |
| atendida_por | FK → User | Operador asignado (opcional) |

#### Cliente
Datos del ciudadano registrado en el totem.

| Campo | Tipo | Descripción |
|---|---|---|
| rut | CharField(12) | RUN chileno (ej: 14.333.671-9) |
| nombre_completo | CharField(200) | Nombre completo |
| fecha_nacimiento | DateField | Fecha de nacimiento |
| telefono | CharField(15) | Teléfono de contacto |
| email | EmailField | Correo electrónico (opcional) |
| observaciones | TextField | Notas adicionales |
| creado_en | DateTimeField | Timestamp de registro |

#### Turno
Unidad central del sistema — representa un turno de atención.

| Campo | Tipo | Descripción |
|---|---|---|
| codigo | CharField(5) | Código único (1 letra + 4 dígitos, ej: A0023) |
| cliente | FK → Cliente | Cliente asociado |
| es_preferencial | BooleanField | Si es atención preferencial |
| estado | CharField(20) | esperando / llamado / atendiendo / completado / cancelado |
| mesa | FK → Mesa | Mesa donde se atiende |
| atendido_por | FK → User | Operador que atendió |
| creado_en | DateTimeField | Momento de creación |
| llamado_en | DateTimeField | Momento del llamado |
| completado_en | DateTimeField | Momento de finalización |

**Ciclo de vida del turno:**
```
esperando → llamado → completado
                   ↘ cancelado (si se llama otro en la misma mesa)
```

#### LogAtencion
Registro de auditoría de todas las acciones del sistema.

| Campo | Tipo | Descripción |
|---|---|---|
| turno | FK → Turno | Turno relacionado |
| usuario | FK → User | Operador que ejecutó la acción |
| accion | CharField(100) | Tipo: llamado, rellamado, completado, cancelado, datos_actualizados |
| detalle | TextField | Descripción detallada |
| timestamp | DateTimeField | Momento de la acción |

### 3.2 Modelos de Configuración de Pantalla

#### LogoPantalla
Logos de sponsors/instituciones para la pantalla de llamado.

| Campo | Tipo | Descripción |
|---|---|---|
| nombre | CharField(100) | Nombre del sponsor |
| imagen | ImageField | Archivo de imagen (upload a media/logos/) |
| activo | BooleanField | Visible o no |
| orden | IntegerField | Orden de aparición |

#### MarquesinaPantalla
Textos desplazables en la pantalla de llamado.

| Campo | Tipo | Descripción |
|---|---|---|
| texto | CharField(500) | Contenido del mensaje |
| color | CharField(20) | Color hex del texto |
| velocidad | IntegerField | Duración del recorrido en segundos (8/12/20/30) |
| tamano_fuente | CharField(10) | Tamaño CSS (ej: 1.3rem) |
| activo | BooleanField | Visible o no |
| orden | IntegerField | Orden de concatenación |

Múltiples marquesinas activas se concatenan con separador ★.

#### VideoPantalla
Videos de YouTube/Vimeo para reproducir en la pantalla.

| Campo | Tipo | Descripción |
|---|---|---|
| titulo | CharField(200) | Título descriptivo |
| url | URLField | URL de YouTube o Vimeo |
| activo | BooleanField | En rotación o no |
| orden | IntegerField | Orden de reproducción |

#### ConfigVideoPantalla (Singleton)
Configuración global del reproductor de video.

| Campo | Tipo | Descripción |
|---|---|---|
| modo_reproduccion | CharField | secuencial / aleatorio |
| volumen | IntegerField | 0-100 |
| habilitado | BooleanField | Activar/desactivar reproductor |

**Modo aleatorio:** Usa algoritmo Fisher-Yates para barajar todos los videos. Reproduce la lista completa antes de rebarajar, garantizando que todos los videos se vean antes de repetir.

#### ConfigApariencia (Singleton)
Configuración global de colores y tipografía de toda la aplicación.

| Sección | Campos |
|---|---|
| Pantalla - Fondo | pantalla_fondo, pantalla_call_grad1/2, pantalla_espera_grad1/2 |
| Pantalla - Código | pantalla_codigo_color, _fuente, _tamano |
| Pantalla - Nombre | pantalla_nombre_color, _fuente, _tamano |
| Pantalla - Mesa | pantalla_mesa_color, _fuente, _tamano |
| Pantalla - Historial | pantalla_historial_codigo, _nombre, _mesa |
| Navbar | nav_grad1, nav_grad2 |
| Totem | totem_fondo_grad1/2/3, totem_header_grad1/2 |
| Botones | btn_llamar_grad1/2, btn_completar_grad1/2, btn_guardar_grad1/2 |
| Turno Confirmado | confirmado_esperando/llamado/completado/cancelado_grad1/2 |

Los valores se sirven via API `/api/apariencia/` y se aplican como CSS variables en `:root`.

---

## 4. INTERFACES DEL SISTEMA

### 4.1 Totem — Registro de Clientes (`/`)

**Propósito:** Punto de entrada del cliente. Permite registrarse mediante lectura OCR de cédula o ingreso manual.

**Funcionalidades:**
- Cámara con enfoque continuo (1920x1080, cámara trasera).
- Lectura automática de MRZ (Machine Readable Zone) del reverso de la cédula chilena (formato TD1, ICAO Doc 9303).
- Escaneo continuo cada 1.5 segundos con validación automática.
- Recorte del 40% inferior de la imagen (zona MRZ) con binarización para mejorar OCR.
- Guía visual verde para posicionamiento del MRZ.
- Panel de debug OCR para diagnóstico.
- Formulario manual como alternativa.
- Detección automática de atención preferencial (60+ años basado en fecha de nacimiento).

**Algoritmo de parseo MRZ:**
1. Concatenar todo el texto sin saltos de línea.
2. Limpiar caracteres no válidos, convertir a mayúsculas.
3. Split por `<`, filtrar tokens vacíos.
4. Leer desde el final: [-1]=nombre2, [-2]=nombre1, [-3]=materno, [-4]=paterno.
5. Token [-7]: primeros 6 chars = fecha YYMMDD, últimos 8 dígitos = RUN.
6. Token [-6]: dígito verificador del RUN.

### 4.2 Turno Confirmado — Celular (`/turno-confirmado/<id>/`)

**Propósito:** Página que el cliente ve en su celular después de registrarse. Muestra el estado del turno en tiempo real.

**Funcionalidades:**
- Polling cada 3 segundos al endpoint `/api/estado-turno/<id>/`.
- Estados visuales con colores dinámicos (CSS variables):
  - **Esperando:** Fondo verde, ícono reloj.
  - **Llamado:** Fondo naranja, alerta fullscreen de 5 segundos, vibración del dispositivo (patrón 500-200-500-200-500ms).
  - **Atendiendo:** Fondo naranja, ícono persona.
  - **Completado:** Fondo azul, mensaje de agradecimiento, botón nuevo turno.
  - **Cancelado:** Fondo rojo, mensaje de turno expirado, botón nuevo turno.
- Badge "⭐ Atención Preferencial" si aplica.

### 4.3 Pantalla de Llamado (`/pantalla/`)

**Propósito:** Display grande (TV/monitor) para visualización pública de los llamados.

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ [Logos]  [Marquesina desplazable...]  [🔊] [14:30:25]  │
├───────────────────────────────┬─────────────────────────┤
│                               │  ┌───────────────────┐  │
│                               │  │   En Espera: 5    │  │
│        A 4 3 9 3              │  └───────────────────┘  │
│                               │  ┌───────────────────┐  │
│    Eduardo Arevalo Salgado    │  │ Últimos Llamados  │  │
│                               │  │ R7968 BREND...    │  │
│       ➜ Mesa 2                │  │ N1512 Mauricio... │  │
│                               │  └───────────────────┘  │
│                               │  ┌───────────────────┐  │
│                               │  │  [Video Player]   │  │
│                               │  └───────────────────┘  │
├───────────────────────────────┴─────────────────────────┤
│                              Powered by TotemIA 2026    │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Polling cada 3 segundos a `/api/turnos-activos/`.
- Audio `belldoor.wav` al detectar nuevo llamado o rellamado (detecta cambio en `llamado_en`).
- Botón "Activar Sonido" para desbloquear autoplay del navegador.
- Logos de sponsors dinámicos (recarga cada 60s).
- Marquesina con múltiples textos concatenados.
- Reproductor de video YouTube/Vimeo integrado:
  - Mute automático durante el audio de llamado.
  - Restauración de volumen al terminar el audio.
  - Modo secuencial o aleatorio (Fisher-Yates).
  - Soporte YouTube IFrame API y Vimeo Player API.
- Badge "⭐ Atención Preferencial" en llamado actual e historial.
- Reloj en tiempo real con estilo prominente.
- Scrollbar estilizada en el historial.
- Todos los colores y tipografías configurables via CSS variables.

### 4.4 Mesa de Atención (`/mesa/`) — Requiere login

**Propósito:** Interfaz del operador para gestionar la atención de turnos.

**Funcionalidades:**
- Selector de mesa con persistencia en localStorage.
- Toggle preferencial en vivo (Normal / ⭐ Preferencial).
- Botón "Llamar Siguiente":
  - Cancela automáticamente turnos anteriores en la mesa.
  - Si mesa es preferencial, prioriza clientes 60+ años.
  - Fallback a cola normal si no hay preferenciales.
- Card de turno actual con:
  - Código del turno y badge preferencial.
  - Formulario editable: nombre, RUT, fecha nacimiento, teléfono, email, observaciones.
  - Botones: Guardar, Rellamar, Completar.
- Cola de espera en tiempo real (polling 5s) con badges preferenciales.
- Recuperación automática del turno activo al recargar la página.
- Exportar Excel (solo admin).

### 4.5 Panel de Administración (`/admin-panel/`) — Requiere login

**Propósito:** Dashboard con métricas y gestión. Vista diferenciada para admin y operador.

**Indicadores globales (todos):**
- Turnos hoy, en espera, atendidos.

**Dashboard del operador (todos):**
- Mis atendidos, cancelados, promedio de atención, total semana.
- Gráfico de atenciones por hora (barras).
- Gráfico de últimos 7 días (línea).
- Gráfico preferenciales vs normales (donut).
- Gráfico atenciones por mesa (barras horizontales).

**Tabla de datos (solo admin):**
- Tabla completa de turnos del día con columna preferencial.
- Exportar a Excel con filtros de fecha.

**Acceso restringido (solo admin):**
- Logs de auditoría.
- Exportación Excel.

### 4.6 Django Admin (`/django-admin/`)

**Modelos administrables:**
- Mesas, Clientes, Turnos, Logs de Atención.
- Logos Pantalla (upload de imágenes, orden, activo).
- Marquesinas Pantalla (texto, color, velocidad, tamaño, orden).
- Videos Pantalla (URL YouTube/Vimeo, orden, activo).
- Configuración Video (modo, volumen, habilitado) — singleton.
- Configuración Apariencia (colores y tipografía) — singleton con fieldsets organizados.
- Usuarios con acciones masivas: otorgar/revocar staff.

---

## 5. API REST

Todas las APIs retornan JSON.

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/registrar-turno/` | Registrar cliente y generar turno | No |
| GET | `/api/turnos-activos/` | Turno actual + historial + espera | No |
| GET | `/api/turnos-espera/` | Lista de turnos en espera | No |
| GET | `/api/turno-actual/?mesa_id=X` | Turno activo en una mesa | No |
| GET | `/api/estado-turno/<id>/` | Estado de un turno (polling celular) | No |
| POST | `/api/llamar-turno/` | Llamar siguiente turno | Session |
| POST | `/api/rellamar-turno/` | Rellamar turno actual | Session |
| POST | `/api/completar-turno/` | Marcar turno como completado | Session |
| POST | `/api/actualizar-cliente/` | Editar datos del cliente | Session |
| POST | `/api/toggle-preferencial/` | Cambiar modo preferencial de mesa | Session |
| GET | `/api/logos-pantalla/` | Logos + marquesinas activos | No |
| GET | `/api/videos-pantalla/` | Videos + config del reproductor | No |
| GET | `/api/apariencia/` | Configuración de colores/tipografía | No |
| GET | `/api/mis-estadisticas/` | Métricas del operador actual | Session |
| GET | `/admin-panel/exportar-excel/` | Exportar turnos a Excel | Admin |

---

## 6. FLUJO DE ATENCIÓN

### 6.1 Flujo Normal
1. Cliente se acerca al totem y posiciona el reverso de su cédula.
2. El sistema lee el MRZ automáticamente y extrae: nombre, RUN, fecha de nacimiento.
3. Cliente completa teléfono y confirma registro.
4. Sistema genera turno (código único) y determina si es preferencial (60+ años).
5. Cliente recibe página de confirmación en su celular con polling de estado.
6. Operador en mesa presiona "Llamar Siguiente".
7. Si la mesa es preferencial, se prioriza al cliente de mayor edad en la cola.
8. Pantalla grande muestra el código + nombre + mesa con audio.
9. Celular del cliente vibra y muestra alerta fullscreen.
10. Operador atiende, puede editar datos, y presiona "Completar".
11. Cliente ve en su celular "Atención completada".

### 6.2 Flujo Preferencial
- Al registrarse, si el cliente tiene 60+ años, el turno se marca como `es_preferencial=True`.
- Las mesas con toggle preferencial activado buscan primero turnos preferenciales.
- Si no hay preferenciales, atienden el siguiente normal.
- Badges ⭐ visibles en: cola de espera, turno actual, pantalla, celular, admin.

### 6.3 Cancelación Automática
- Al llamar un nuevo turno en una mesa, cualquier turno anterior (llamado o atendiendo) se cancela automáticamente.
- El cliente anterior ve en su celular "Turno pasado" con opción de solicitar nuevo turno.
- Se registra en el log de auditoría.

---

## 7. SEGURIDAD

### 7.1 Autenticación
- Login basado en sesiones Django (`django.contrib.auth`).
- Vistas de mesa y admin protegidas con `@login_required`.
- Exportación Excel y logs restringidos a `is_superuser`.
- Acciones masivas de staff en Django Admin.

### 7.2 CSRF
- Protección CSRF habilitada en middleware.
- APIs POST usan `@csrf_exempt` (consumidas por JavaScript del mismo origen).
- `CSRF_TRUSTED_ORIGINS` configurado para HTTPS local y zrok.

### 7.3 HTTPS
- Servidor HTTPS custom con certificado autofirmado (desarrollo).
- Soporte para proxy reverso (zrok) con `SECURE_PROXY_SSL_HEADER` y `USE_X_FORWARDED_HOST`.
- Certificado generado con `cryptography` incluyendo SAN para localhost, 127.0.0.1 e IP de red local.

---

## 8. DESPLIEGUE

### 8.1 Desarrollo Local
```bash
python generate_cert.py          # Generar certificado SSL
python manage.py migrate          # Aplicar migraciones
python manage.py createsuperuser  # Crear admin
python run_https.py               # Iniciar en https://0.0.0.0:8443
```

### 8.2 Acceso desde Red Local
- Servidor escucha en `0.0.0.0:8443`.
- Acceso desde celular: `https://<IP_LOCAL>:8443/` (aceptar certificado autofirmado).

### 8.3 Acceso Público (zrok)
```bash
zrok share public localhost:8000
```
- Django configurado con `ALLOWED_HOSTS = ['.zrok.io']`.
- `CSRF_TRUSTED_ORIGINS` incluye `https://*.zrok.io`.
- Headers de proxy reverso habilitados.

### 8.4 Servidor HTTPS Custom (`run_https.py`)
- Basado en `wsgiref.simple_server` + `ssl.SSLContext`.
- `StaticFilesHandler` para servir archivos estáticos (CSS/JS del Django Admin).
- `MediaStaticHandler` custom para servir archivos de `/media/` (logos subidos).

---

## 9. DEPENDENCIAS

| Paquete | Uso |
|---|---|
| Django 5.x | Framework web |
| openpyxl | Exportación Excel |
| cryptography | Generación de certificados SSL |
| Pillow | Procesamiento de imágenes (ImageField) |

**CDN (frontend):**
- MaterializeCSS 1.0
- Google Fonts (Roboto)
- Material Icons
- Tesseract.js 5
- Chart.js 4
- YouTube IFrame API
- Vimeo Player API

---

## 10. CONFIGURACIÓN AUTOADMINISTRABLE

El sistema está diseñado para ser completamente autoadministrable desde Django Admin sin intervención técnica:

| Elemento | Administración |
|---|---|
| Mesas | Crear, activar/desactivar, asignar operador |
| Modo preferencial | Toggle en vivo desde interfaz de mesa |
| Usuarios | Crear, revocar/otorgar staff masivamente |
| Logos | Subir imágenes, ordenar, activar/desactivar |
| Marquesinas | Múltiples textos, color, velocidad, tamaño |
| Videos | URLs YouTube/Vimeo, modo secuencial/aleatorio, volumen |
| Colores | Todos los gradientes, fondos y colores de texto |
| Tipografía | Fuente y tamaño del código, nombre y mesa en pantalla |
| Audio | Archivo `belldoor.wav` reemplazable en `/static/` |

---

## 11. CARACTERÍSTICAS DESTACADAS

1. **OCR de cédula chilena** con lectura MRZ automática (Tesseract.js client-side).
2. **Atención preferencial** automática basada en edad del cliente.
3. **Notificación móvil** en tiempo real con vibración y alerta fullscreen.
4. **Reproductor multimedia** integrado con mute inteligente durante llamados.
5. **Tema visual dinámico** completamente configurable desde admin.
6. **Múltiples marquesinas** concatenables con separador visual.
7. **Logos de sponsors** dinámicos y opcionales.
8. **Dashboard con métricas** diferenciado para admin y operador.
9. **Exportación Excel** con filtros de fecha.
10. **Auditoría completa** de todas las acciones del sistema.
11. **Recuperación de sesión** — el operador no pierde el turno activo al navegar.
12. **Rellamado** — permite volver a llamar al mismo turno con audio y notificación.
13. **Cancelación automática** — al llamar nuevo turno, el anterior se cancela.
14. **Acceso público** via zrok sin configuración adicional.
