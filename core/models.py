import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Mesa(models.Model):
    """Mesa/punto de atención"""
    nombre = models.CharField(max_length=50)
    activa = models.BooleanField(default=True)
    preferencial = models.BooleanField(default=False, help_text='Atiende preferentemente a tercera edad (60+ años)')
    edad_preferencial = models.IntegerField(default=60, help_text='Edad mínima para atención preferencial')
    atendida_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='mesas'
    )

    def __str__(self):
        pref = ' ⭐' if self.preferencial else ''
        return f"{self.nombre}{pref}"

    class Meta:
        ordering = ['nombre']


class Cliente(models.Model):
    """Datos del cliente registrado en el totem"""
    rut = models.CharField(max_length=12, blank=True)
    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rut})"

    class Meta:
        ordering = ['-creado_en']


class Turno(models.Model):
    """Turno de atención generado"""
    ESTADO_CHOICES = [
        ('esperando', 'Esperando'),
        ('llamado', 'Llamado'),
        ('atendiendo', 'Atendiendo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    codigo = models.CharField(max_length=5, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='turnos')
    es_preferencial = models.BooleanField(default=False, help_text='Cliente de atención preferencial')
    motivo_preferencial = models.CharField(max_length=30, blank=True, default='', help_text='Motivo: edad, solicitud, o vacío')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='esperando')
    mesa = models.ForeignKey(Mesa, on_delete=models.SET_NULL, null=True, blank=True)
    atendido_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='turnos_atendidos'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    llamado_en = models.DateTimeField(null=True, blank=True)
    completado_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.cliente.nombre_completo}"

    class Meta:
        ordering = ['-creado_en']

    @staticmethod
    def generar_codigo():
        """Genera código único: 1 letra + 4 números (ej: A0023)"""
        while True:
            letra = random.choice(string.ascii_uppercase)
            numeros = f"{random.randint(0, 9999):04d}"
            codigo = f"{letra}{numeros}"
            if not Turno.objects.filter(codigo=codigo).exists():
                return codigo


class LogAtencion(models.Model):
    """Log de acciones para auditoría"""
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, related_name='logs')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=100)
    detalle = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.accion}"

    class Meta:
        ordering = ['-timestamp']


class LogoPantalla(models.Model):
    """Logos de sponsors para mostrar en la pantalla de llamado"""
    nombre = models.CharField(max_length=100, help_text='Nombre del sponsor/logo')
    imagen = models.ImageField(upload_to='logos/', help_text='Imagen del logo (PNG/JPG)')
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0, help_text='Orden de aparición (menor = primero)')

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['orden']
        verbose_name = 'Logo Pantalla'
        verbose_name_plural = 'Logos Pantalla'


class MarquesinaPantalla(models.Model):
    """Texto de marquesina para la pantalla de llamado"""
    VELOCIDAD_CHOICES = [
        (30, 'Lenta'),
        (20, 'Normal'),
        (12, 'Rápida'),
        (8, 'Muy rápida'),
    ]

    texto = models.CharField(max_length=500, help_text='Texto a mostrar en la marquesina')
    color = models.CharField(max_length=20, default='#ffffff', help_text='Color del texto (hex, ej: #ffca28)')
    velocidad = models.IntegerField(default=20, choices=VELOCIDAD_CHOICES, help_text='Duración en segundos del recorrido (menor = más rápido)')
    tamano_fuente = models.CharField(max_length=10, default='1.3rem', help_text='Tamaño de fuente CSS (ej: 1.3rem, 18px, 1.5em)')
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0, help_text='Orden de aparición (menor = primero)')

    def __str__(self):
        return self.texto[:50]

    class Meta:
        ordering = ['orden']
        verbose_name = 'Marquesina Pantalla'
        verbose_name_plural = 'Marquesinas Pantalla'


class VideoPantalla(models.Model):
    """Videos de YouTube/Vimeo para reproducir en la pantalla de llamado"""
    ORDEN_CHOICES = [
        ('secuencial', 'Secuencial'),
        ('aleatorio', 'Aleatorio'),
    ]

    titulo = models.CharField(max_length=200, help_text='Título descriptivo del video')
    url = models.URLField(help_text='URL de YouTube o Vimeo (ej: https://www.youtube.com/watch?v=xxx)')
    activo = models.BooleanField(default=True)
    orden = models.IntegerField(default=0, help_text='Orden de reproducción (menor = primero)')

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['orden']
        verbose_name = 'Video Pantalla'
        verbose_name_plural = 'Videos Pantalla'


class ConfigVideoPantalla(models.Model):
    """Configuración global del reproductor de video en pantalla"""
    MODO_CHOICES = [
        ('secuencial', 'Secuencial'),
        ('aleatorio', 'Aleatorio'),
    ]

    modo_reproduccion = models.CharField(max_length=20, choices=MODO_CHOICES, default='secuencial')
    volumen = models.IntegerField(default=30, help_text='Volumen del video (0-100)')
    habilitado = models.BooleanField(default=True, help_text='Activar/desactivar el reproductor')

    def __str__(self):
        return f'Config Video - {self.modo_reproduccion} - Vol:{self.volumen}'

    class Meta:
        verbose_name = 'Configuración Video'
        verbose_name_plural = 'Configuración Video'


class ConfigApariencia(models.Model):
    """Configuración global de colores y tipografía de la aplicación"""

    # --- Pantalla de llamado ---
    pantalla_fondo = models.CharField(max_length=20, default='#0d1b2a', help_text='Fondo pantalla de llamado')
    pantalla_call_grad1 = models.CharField(max_length=20, default='#1565c0', help_text='Gradiente llamado color 1')
    pantalla_call_grad2 = models.CharField(max_length=20, default='#0d47a1', help_text='Gradiente llamado color 2')
    pantalla_codigo_color = models.CharField(max_length=20, default='#ffffff', help_text='Color del código de turno')
    pantalla_codigo_fuente = models.CharField(max_length=100, default='Roboto, sans-serif', help_text='Tipografía del código')
    pantalla_codigo_tamano = models.CharField(max_length=20, default='10rem', help_text='Tamaño del código (ej: 10rem)')
    pantalla_nombre_color = models.CharField(max_length=20, default='#ffca28', help_text='Color del nombre del cliente')
    pantalla_nombre_fuente = models.CharField(max_length=100, default='Roboto, sans-serif', help_text='Tipografía del nombre')
    pantalla_nombre_tamano = models.CharField(max_length=20, default='3rem', help_text='Tamaño del nombre')
    pantalla_mesa_color = models.CharField(max_length=20, default='#81d4fa', help_text='Color de la mesa')
    pantalla_mesa_fuente = models.CharField(max_length=100, default='Roboto, sans-serif', help_text='Tipografía de la mesa')
    pantalla_mesa_tamano = models.CharField(max_length=20, default='4rem', help_text='Tamaño de la mesa')
    pantalla_espera_grad1 = models.CharField(max_length=20, default='#ff6f00', help_text='Gradiente caja espera color 1')
    pantalla_espera_grad2 = models.CharField(max_length=20, default='#ff8f00', help_text='Gradiente caja espera color 2')
    pantalla_historial_codigo = models.CharField(max_length=20, default='#ffca28', help_text='Color código en historial')
    pantalla_historial_nombre = models.CharField(max_length=20, default='#e0e0e0', help_text='Color nombre en historial')
    pantalla_historial_mesa = models.CharField(max_length=20, default='#81d4fa', help_text='Color mesa en historial')

    # --- Navbar (mesa y admin) ---
    nav_grad1 = models.CharField(max_length=20, default='#1565c0', help_text='Gradiente navbar color 1')
    nav_grad2 = models.CharField(max_length=20, default='#0d47a1', help_text='Gradiente navbar color 2')

    # --- Totem (registro) ---
    totem_fondo_grad1 = models.CharField(max_length=20, default='#0d47a1', help_text='Gradiente fondo totem color 1')
    totem_fondo_grad2 = models.CharField(max_length=20, default='#1565c0', help_text='Gradiente fondo totem color 2')
    totem_fondo_grad3 = models.CharField(max_length=20, default='#1e88e5', help_text='Gradiente fondo totem color 3')
    totem_header_grad1 = models.CharField(max_length=20, default='#ff6f00', help_text='Gradiente header totem color 1')
    totem_header_grad2 = models.CharField(max_length=20, default='#ff8f00', help_text='Gradiente header totem color 2')

    # --- Botones globales ---
    btn_llamar_grad1 = models.CharField(max_length=20, default='#ff6f00', help_text='Botón llamar color 1')
    btn_llamar_grad2 = models.CharField(max_length=20, default='#ff8f00', help_text='Botón llamar color 2')
    btn_completar_grad1 = models.CharField(max_length=20, default='#2e7d32', help_text='Botón completar color 1')
    btn_completar_grad2 = models.CharField(max_length=20, default='#43a047', help_text='Botón completar color 2')
    btn_guardar_grad1 = models.CharField(max_length=20, default='#1565c0', help_text='Botón guardar color 1')
    btn_guardar_grad2 = models.CharField(max_length=20, default='#1e88e5', help_text='Botón guardar color 2')

    # --- Turno confirmado ---
    confirmado_esperando_grad1 = models.CharField(max_length=20, default='#2e7d32', help_text='Fondo esperando color 1')
    confirmado_esperando_grad2 = models.CharField(max_length=20, default='#43a047', help_text='Fondo esperando color 2')
    confirmado_llamado_grad1 = models.CharField(max_length=20, default='#e65100', help_text='Fondo llamado color 1')
    confirmado_llamado_grad2 = models.CharField(max_length=20, default='#ff6f00', help_text='Fondo llamado color 2')
    confirmado_completado_grad1 = models.CharField(max_length=20, default='#1565c0', help_text='Fondo completado color 1')
    confirmado_completado_grad2 = models.CharField(max_length=20, default='#1e88e5', help_text='Fondo completado color 2')
    confirmado_cancelado_grad1 = models.CharField(max_length=20, default='#b71c1c', help_text='Fondo cancelado color 1')
    confirmado_cancelado_grad2 = models.CharField(max_length=20, default='#e53935', help_text='Fondo cancelado color 2')

    # --- Footer pantalla ---
    pantalla_footer_texto = models.CharField(max_length=200, default='Powered by TotemIA 2026', help_text='Texto del footer en la pantalla de llamado')

    def __str__(self):
        return 'Configuración de Apariencia'

    class Meta:
        verbose_name = 'Configuración Apariencia'
        verbose_name_plural = 'Configuración Apariencia'
