# TotemIA — Memoria Técnica del Sistema

## Documento de Arquitectura, Diseño, Funcionamiento y Características

**Versión:** 1.1  
**Fecha:** Marzo 2026  
**Plataforma:** Django 5.x / Python 3.13 / SQLite  
**Repositorio:** https://github.com/marcoarevalozambrano/TotemIA  
**Autor del desarrollo:** Asistido por IA (Kiro)

---

## 1. DESCRIPCIÓN GENERAL

TotemIA es un sistema de gestión de turnos y atención al público diseñado para entornos presenciales (oficinas de atención, instituciones educativas, servicios públicos). El sistema permite el registro de clientes mediante lectura OCR de cédula de identidad chilena (MRZ), la asignación automática de turnos, la visualización en pantalla grande para llamado público, la atención desde mesas de operadores, y la notificación en tiempo real al cliente en su dispositivo móvil.

### 1.1 Objetivos del Sistema
- Automatizar el flujo de atención de público con registro digital.
- Reducir tiempos de espera mediante priorización preferencial (tercera edad y Ley N° 21.168).
- Proveer visibilidad en tiempo real del estado de la cola.
- Permitir notificación directa al cliente en su celular.
- Ofrecer una plataforma completamente autoadministrable sin intervención técnica.
- Soportar contenido multimedia configurable (videos, logos, marquesinas).

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
│   ├── urls.py                # URLs raíz (+ media serving)
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
├── core/                      # Aplicación principal
│   ├── models.py              # 11 modelos de datos
│   ├── views.py               # 22 vistas y APIs
│   ├── urls.py                # 20 rutas de la aplicación
│   ├── admin.py               # Configuración Django Admin personalizada
│   └── migrations/            # 9 migraciones de BD
├── templates/
│   ├── base.html              # Template base con tema dinámico (CSS variables)
│   └── core/
│       ├── totem.html          # Interfaz de registro (totem + OCR)
│       ├── turno_confirmado.html # Confirmación en celular (polling)
│       ├── pantalla.html       # Pantalla de llamado (multimedia)
│       ├── mesa.html           # Interfaz del operador
│       ├── admin_panel.html    # Panel de administración (Chart.js)
│       ├── login.html          # Login
│       └── logs.html           # Visor de logs de auditoría
├── static/
│   ├── belldoor.wav           # Audio de llamado
│   ├── favicon/               # Favicon (ico, png, webmanifest)
│   └── logos/                 # Logos estáticos
├── media/                     # Archivos subidos (logos dinámicos)
├── run_https.py               # Servidor HTTPS desarrollo (static + media)
├── generate_cert.py           # Generador de certificados SSL (SAN configurable)
├── cargar_usuarios.py         # Script de carga masiva de usuarios
├── MEMORIA_TECNICA.md         # Este documento
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
│ Preferencial │     │ Logos+Marq.  │     │ Alertas         │
└──────┬───────┘     └──────┬───────┘     └────────┬────────┘
       │                    │                      │
       │         ┌──────────┴──────────┐           │
       └─────────┤   DJANGO BACKEND    ├───────────┘
                 │                     │
                 │  22 APIs REST/JSON  │
                 │  SQLite + 11 modelos│
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
       │  Preferencial │          │  Gestión       │
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
| preferencial | BooleanField | Si prioriza atención preferencial |
| edad_preferencial | IntegerField | Edad mínima para prioridad automática (default: 60) |
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
| motivo_preferencial | CharField(30) | Motivo: `edad`, `solicitud`, `edad+solicitud`, o vacío |
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

**Motivos preferenciales:**
- `edad` — Cliente de 60+ años (detección automática por fecha de nacimiento)
- `solicitud` — Solicitud manual del cliente (Ley N° 21.168: discapacidad, embarazo, etc.)
- `edad+solicitud` — Ambas condiciones aplican

**Iconografía por motivo:**
- ⭐ = edad (tercera edad)
- ♿ = solicitud manual
- 👴♿ = ambos

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
Textos desplazables en la pantalla de llamado. Cada marquesina tiene su propia configuración visual.

| Campo | Tipo | Descripción |
|---|---|---|
| texto | CharField(500) | Contenido del mensaje (soporta emojis Unicode) |
| color | CharField(20) | Color hex del texto (individual por marquesina) |
| velocidad | IntegerField | Duración del recorrido en segundos (8/12/20/30) |
| tamano_fuente | CharField(10) | Tamaño CSS individual (ej: 1.3rem) |
| activo | BooleanField | Visible o no |
| orden | IntegerField | Orden de aparición |

Múltiples marquesinas activas se renderizan con su propio color y tamaño, separadas por ★. La velocidad se ajusta automáticamente al largo total del texto concatenado.

#### VideoPantalla
Videos de YouTube/Vimeo para reproducir en la pantalla.

| Campo | Tipo | Descripción |
|---|---|---|
| titulo | CharField(200) | Título descriptivo |
| url | URLField | URL de YouTube o Vimeo |
| activo | BooleanField | En rotación o no |
| orden | IntegerField | Orden de reproducción |

URLs soportadas: `youtube.com/watch?v=`, `youtu.be/`, `youtube.com/embed/`, `vimeo.com/`, `vimeo.com/video/`.

#### ConfigVideoPantalla (Singleton)
Configuración global del reproductor de video.

| Campo | Tipo | Descripción |
|---|---|---|
| modo_reproduccion | CharField | secuencial / aleatorio |
| volumen | IntegerField | 0-100 |
| habilitado | BooleanField | Activar/desactivar reproductor |

**Modo aleatorio:** Usa algoritmo Fisher-Yates para barajar todos los videos. Reproduce la lista completa antes de rebarajar, garantizando que todos los N videos se vean antes de repetir alguno. Evita repetir el último video al inicio de la nueva baraja.

**Comportamiento de audio:** El video se mutea automáticamente cuando suena `belldoor.wav` (llamado/rellamado) y se restaura el volumen configurado al terminar el audio. La reproducción del video no se interrumpe.

#### ConfigApariencia (Singleton)
Configuración global de colores, tipografía y textos de toda la aplicación.

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
| Footer Pantalla | pantalla_footer_texto (default: "Powered by TotemIA 2026") |

Los valores se sirven via API `/api/apariencia/` y se aplican como CSS variables en `:root` al cargar cualquier página. El footer de la pantalla es configurable para mostrar texto institucional personalizado.

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
- Toggle de solicitud preferencial manual con ícono ♿ (Ley N° 21.168) para discapacidad, embarazo u otra condición.
- Favicon personalizado.

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
- Estados visuales con colores dinámicos (CSS variables configurables):
  - **Esperando:** Fondo verde, ícono reloj.
  - **Llamado:** Fondo naranja, alerta fullscreen de 5 segundos, vibración del dispositivo (patrón 500-200-500-200-500ms).
  - **Atendiendo:** Fondo naranja, ícono persona.
  - **Completado:** Fondo azul, mensaje de agradecimiento, botón nuevo turno.
  - **Cancelado:** Fondo rojo, mensaje de turno expirado, botón nuevo turno.
- Badge preferencial con ícono según motivo (⭐/♿/👴♿).

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
│       ➜ Mesa 2                │  │ N1512 Mauricio ⭐ │  │
│                               │  └───────────────────┘  │
│                               │  ┌───────────────────┐  │
│                               │  │  [Video Player]   │  │
│                               │  └───────────────────┘  │
├───────────────────────────────┴─────────────────────────┤
│                    [Footer configurable desde admin]    │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- Polling cada 3 segundos a `/api/turnos-activos/`.
- Audio `belldoor.wav` al detectar nuevo llamado o rellamado (detecta cambio en `llamado_en`).
- Botón "Activar Sonido" para desbloquear autoplay del navegador.
- Logos de sponsors dinámicos alineados a la izquierda (recarga cada 60s).
- Múltiples marquesinas con color y tamaño individual, separadas por ★, velocidad auto-ajustada al largo del texto.
- Soporte de emojis Unicode en marquesinas.
- Reproductor de video YouTube/Vimeo integrado:
  - Mute automático durante el audio de llamado, restauración al terminar.
  - Modo secuencial o aleatorio (Fisher-Yates, reproduce todos antes de repetir).
  - Soporte YouTube IFrame API y Vimeo Player API para detección de fin de video.
  - Configuración de volumen desde admin.
- Badge preferencial con ícono según motivo en llamado actual e historial.
- Historial incluye turnos cancelados (con opacidad reducida).
- Reloj prominente con relieve y fondo semi-transparente.
- Scrollbar estilizada en el historial (delgada, semi-transparente).
- Footer configurable desde Django Admin.
- Todos los colores, tipografías y tamaños configurables via CSS variables.

### 4.4 Mesa de Atención (`/mesa/`) — Requiere login

**Propósito:** Interfaz del operador para gestionar la atención de turnos.

**Funcionalidades:**
- Selector de mesa con persistencia en localStorage (se recuerda al recargar).
- Toggle preferencial en vivo (Normal / ⭐ Preferencial) con API instantánea.
- Botón "Llamar Siguiente":
  - Cancela automáticamente turnos anteriores en la mesa (llamados o atendiendo).
  - Si mesa es preferencial, prioriza clientes preferenciales (edad o solicitud).
  - Fallback a cola normal si no hay preferenciales.
- Card de turno actual con:
  - Código del turno y badge preferencial con ícono según motivo (⭐/♿/👴♿).
  - Formulario editable: nombre, RUT, fecha nacimiento, teléfono, email, observaciones.
  - Botones: Guardar, Rellamar (re-trigger audio y notificación), Completar.
- Cola de espera paginada (20 por página, botón "Cargar más"):
  - Contador total con desglose preferencial.
  - Si mesa es preferencial, preferenciales aparecen primero con fondo amarillo y separador visual "Cola normal".
  - Badges con ícono según motivo.
  - Scrollbar estilizada.
  - Hora en zona horaria local (America/Santiago).
- Recuperación automática del turno activo al recargar la página (consulta `/api/turno-actual/`).
- Exportar Excel (solo admin).

### 4.5 Panel de Administración (`/admin-panel/`) — Requiere login

**Propósito:** Dashboard con métricas y gestión. Vista diferenciada para admin y operador.

**Indicadores globales (todos):**
- Turnos hoy, en espera, atendidos.

**Dashboard del operador (todos):**
- Mis atendidos, cancelados, promedio de atención, total semana.
- Gráfico de flujo por hora: ingresados vs completados (barras).
- Gráfico de últimos 7 días (línea).
- Gráfico preferenciales vs normales (donut).
- Snapshot de mesas: estado actual, operador, turno en atención, promedio.

**Tabla de datos (solo admin):**
- Tabla completa de turnos del día con columna preferencial (ícono según motivo).
- Exportar a Excel con filtros de fecha (incluye columna Motivo).

**Acceso restringido (solo admin):**
- Logs de auditoría.
- Exportación Excel.

### 4.6 Django Admin (`/django-admin/`)

**Modelos administrables:**
- Mesas: nombre, activa, preferencial, edad mínima, operador.
- Clientes: búsqueda por nombre y RUT.
- Turnos: filtros por estado, mesa, preferencial, motivo. Muestra motivo_preferencial.
- Logs de Atención: filtro por acción.
- Logos Pantalla: upload de imágenes, orden editable inline, activo.
- Marquesinas Pantalla: texto (con emojis), color, velocidad, tamaño, orden — todo editable inline.
- Videos Pantalla: URL YouTube/Vimeo, orden, activo — editable inline.
- Configuración Video (singleton): modo, volumen, habilitado.
- Configuración Apariencia (singleton): fieldsets organizados por sección (pantalla, navbar, totem, botones, turno confirmado, footer).
- Usuarios: hereda UserAdmin de Django + acciones masivas ❌ Revocar staff / ✅ Otorgar staff.

---

## 5. API REST

Todas las APIs retornan JSON. Las horas se convierten a zona horaria local (America/Santiago).

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | `/api/registrar-turno/` | Registrar cliente y generar turno (acepta `solicita_preferencial`) | No |
| GET | `/api/turnos-activos/` | Turno actual + historial (incl. cancelados) + espera | No |
| GET | `/api/turnos-espera/?offset=0&limit=20&mesa_id=X` | Lista paginada, ordenada por prioridad si mesa preferencial | No |
| GET | `/api/turno-actual/?mesa_id=X` | Turno activo en una mesa (para recuperación de sesión) | No |
| GET | `/api/estado-turno/<id>/` | Estado de un turno + motivo preferencial (polling celular) | No |
| POST | `/api/llamar-turno/` | Llamar siguiente turno (cancela anteriores) | Session |
| POST | `/api/rellamar-turno/` | Rellamar turno actual (re-trigger audio + notificación) | Session |
| POST | `/api/completar-turno/` | Marcar turno como completado | Session |
| POST | `/api/actualizar-cliente/` | Editar datos del cliente desde mesa | Session |
| POST | `/api/toggle-preferencial/` | Cambiar modo preferencial de mesa en vivo | Session |
| GET | `/api/logos-pantalla/` | Logos activos + marquesinas (individuales con color/tamaño) | No |
| GET | `/api/videos-pantalla/` | Videos activos + config reproductor + embed URLs | No |
| GET | `/api/apariencia/` | Configuración completa de colores/tipografía/footer | No |
| GET | `/api/mis-estadisticas/` | Métricas del operador + flujo por hora + mesas + preferenciales | Session |
| GET | `/admin-panel/exportar-excel/` | Exportar turnos a Excel (con columna Motivo) | Admin |

---

## 6. FLUJO DE ATENCIÓN

### 6.1 Flujo Normal
1. Cliente se acerca al totem y posiciona el reverso de su cédula.
2. El sistema lee el MRZ automáticamente y extrae: nombre, RUN, fecha de nacimiento.
3. Cliente completa teléfono. Si tiene discapacidad u otra condición, activa el toggle ♿ (Ley N° 21.168).
4. Sistema genera turno (código único) y determina si es preferencial (edad 60+ y/o solicitud manual).
5. Cliente recibe página de confirmación en su celular con polling de estado.
6. Operador en mesa presiona "Llamar Siguiente".
7. Si la mesa es preferencial, se priorizan turnos preferenciales (cualquier motivo).
8. Pantalla grande muestra el código + nombre + mesa con audio `belldoor.wav`.
9. Celular del cliente vibra y muestra alerta fullscreen de 5 segundos.
10. Operador atiende, puede editar datos, rellamar si es necesario, y presiona "Completar".
11. Cliente ve en su celular "Atención completada".

### 6.2 Flujo Preferencial (Ley N° 21.168)
Dos vías de activación:
- **Automática por edad:** Si fecha de nacimiento indica 60+ años → motivo `edad` (⭐).
- **Solicitud manual:** Toggle ♿ en el totem → motivo `solicitud` (♿).
- **Ambas:** Si aplican las dos → motivo `edad+solicitud` (👴♿).

Las mesas con toggle preferencial activado buscan primero turnos con `es_preferencial=True` (cualquier motivo), ordenados por hora de llegada. Si no hay preferenciales, atienden el siguiente normal.

En la cola de espera de la mesa preferencial, los turnos preferenciales aparecen primero con fondo amarillo y un separador visual "Cola normal" antes de los turnos regulares.

### 6.3 Cancelación Automática
- Al llamar un nuevo turno en una mesa, cualquier turno anterior (llamado o atendiendo) se cancela automáticamente con `completado_en` registrado.
- El cliente anterior ve en su celular "Turno pasado" (fondo rojo) con opción de solicitar nuevo turno.
- Se registra en el log de auditoría con detalle de la mesa.
- Los turnos cancelados aparecen en el historial de la pantalla (con opacidad reducida).

### 6.4 Rellamado
- El operador puede presionar "Rellamar" para volver a notificar al cliente.
- Actualiza `llamado_en` para que la pantalla detecte el cambio y reproduzca el audio nuevamente.
- El celular del cliente recibe nueva alerta fullscreen con vibración.
- Se registra en el log de auditoría como acción `rellamado`.

---

## 7. SEGURIDAD

### 7.1 Autenticación
- Login basado en sesiones Django (`django.contrib.auth`).
- Vistas de mesa y admin protegidas con `@login_required`.
- Exportación Excel y logs restringidos a `is_superuser`.
- Acciones masivas de staff en Django Admin (otorgar/revocar).
- Script de carga masiva de usuarios (`cargar_usuarios.py`) con contraseña por defecto.

### 7.2 CSRF
- Protección CSRF habilitada en middleware.
- APIs POST usan `@csrf_exempt` (consumidas por JavaScript del mismo origen).
- `CSRF_TRUSTED_ORIGINS` configurado para HTTPS local, IP de red y `*.zrok.io`.

### 7.3 HTTPS
- Servidor HTTPS custom con certificado autofirmado (desarrollo).
- Soporte para proxy reverso (zrok) con `SECURE_PROXY_SSL_HEADER` y `USE_X_FORWARDED_HOST`.
- Certificado generado con `cryptography` incluyendo SAN para localhost, 127.0.0.1 e IP de red local configurable.

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
- IP configurable en `generate_cert.py` (SAN) y `settings.py` (CSRF_TRUSTED_ORIGINS).

### 8.3 Acceso Público (zrok)
```bash
zrok share public localhost:8000
```
- Django configurado con `ALLOWED_HOSTS = ['*', '.zrok.io']`.
- `CSRF_TRUSTED_ORIGINS` incluye `https://*.zrok.io`.
- Headers de proxy reverso habilitados.
- Zona horaria correcta: todas las horas se convierten con `timezone.localtime()`.

### 8.4 Servidor HTTPS Custom (`run_https.py`)
- Basado en `wsgiref.simple_server` + `ssl.SSLContext`.
- `StaticFilesHandler` para servir archivos estáticos (CSS/JS del Django Admin, favicon, audio).
- `MediaStaticHandler` custom (WSGI middleware) para servir archivos de `/media/` (logos subidos).

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

El sistema está diseñado para ser completamente autoadministrable desde Django Admin (`/django-admin/`) sin intervención técnica:

| Elemento | Administración |
|---|---|
| Mesas | Crear, activar/desactivar, asignar operador |
| Modo preferencial | Toggle en vivo desde interfaz de mesa (sin ir al admin) |
| Usuarios | Crear, revocar/otorgar staff masivamente, carga por script |
| Logos | Subir imágenes PNG/JPG, ordenar, activar/desactivar |
| Marquesinas | Múltiples textos con emojis, color individual, velocidad, tamaño, orden |
| Videos | URLs YouTube/Vimeo, modo secuencial/aleatorio, volumen global |
| Colores | Todos los gradientes, fondos y colores de texto de toda la app |
| Tipografía | Fuente y tamaño del código, nombre y mesa en pantalla |
| Footer | Texto configurable en la pantalla de llamado |
| Audio | Archivo `belldoor.wav` reemplazable en `/static/` |

---

## 11. CARACTERÍSTICAS DESTACADAS

1. **OCR de cédula chilena** con lectura MRZ automática (Tesseract.js client-side, formato TD1 ICAO Doc 9303).
2. **Atención preferencial dual:** automática por edad (60+) y solicitud manual (Ley N° 21.168) con iconografía diferenciada (⭐/♿/👴♿).
3. **Notificación móvil** en tiempo real con vibración y alerta fullscreen de 5 segundos.
4. **Reproductor multimedia** integrado (YouTube + Vimeo) con mute inteligente durante llamados y algoritmo Fisher-Yates para reproducción aleatoria completa.
5. **Tema visual dinámico** completamente configurable desde admin (colores, tipografías, tamaños) via CSS variables.
6. **Múltiples marquesinas** con color y tamaño individual, soporte de emojis Unicode, velocidad auto-ajustada.
7. **Logos de sponsors** dinámicos y opcionales, administrables desde Django Admin.
8. **Dashboard con métricas** diferenciado para admin y operador (Chart.js), con flujo por hora, snapshot de mesas, preferenciales.
9. **Exportación Excel** con filtros de fecha y columna de motivo preferencial.
10. **Auditoría completa** de todas las acciones del sistema (llamado, rellamado, cancelado, completado, datos actualizados).
11. **Recuperación de sesión** — el operador no pierde el turno activo al navegar entre páginas.
12. **Rellamado** — permite volver a llamar al mismo turno con audio y notificación al celular.
13. **Cancelación automática** — al llamar nuevo turno, el anterior se cancela y el cliente es notificado.
14. **Cola paginada** — carga de a 20 turnos con botón "Cargar más", ordenamiento preferencial visual.
15. **Acceso público** via zrok sin configuración adicional, con timezone correcto.
16. **Footer configurable** desde Django Admin.
17. **Favicon personalizado** con soporte para todos los dispositivos.
18. **Gestión masiva de usuarios** con acciones de otorgar/revocar staff.
