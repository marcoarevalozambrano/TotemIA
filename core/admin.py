from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Cliente, Turno, Mesa, LogAtencion, LogoPantalla, MarquesinaPantalla, VideoPantalla, ConfigVideoPantalla, ConfigApariencia


# --- Custom User Admin con acciones masivas ---
def revocar_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)
revocar_staff.short_description = '❌ Revocar acceso staff a seleccionados'

def otorgar_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)
otorgar_staff.short_description = '✅ Otorgar acceso staff a seleccionados'

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    actions = [revocar_staff, otorgar_staff]


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'preferencial', 'edad_preferencial', 'atendida_por']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'rut', 'telefono', 'email', 'creado_en']
    search_fields = ['nombre_completo', 'rut']


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'cliente', 'estado', 'mesa', 'atendido_por', 'creado_en']
    list_filter = ['estado', 'mesa']
    search_fields = ['codigo', 'cliente__nombre_completo']


@admin.register(LogAtencion)
class LogAtencionAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'turno', 'usuario', 'accion']
    list_filter = ['accion']


@admin.register(LogoPantalla)
class LogoPantallaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'orden', 'imagen']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']


@admin.register(MarquesinaPantalla)
class MarquesinaPantallaAdmin(admin.ModelAdmin):
    list_display = ['texto', 'color', 'velocidad', 'tamano_fuente', 'orden', 'activo']
    list_editable = ['activo', 'color', 'velocidad', 'tamano_fuente', 'orden']


@admin.register(VideoPantalla)
class VideoPantallaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'url', 'activo', 'orden']
    list_editable = ['activo', 'orden']
    list_filter = ['activo']


@admin.register(ConfigVideoPantalla)
class ConfigVideoPantallaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'modo_reproduccion', 'volumen', 'habilitado']
    list_editable = ['modo_reproduccion', 'volumen', 'habilitado']

    def has_add_permission(self, request):
        # Solo permitir 1 registro de configuración
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(ConfigApariencia)
class ConfigAparienciaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🖥️ Pantalla de Llamado - Fondo y Llamado', {
            'fields': ('pantalla_fondo', 'pantalla_call_grad1', 'pantalla_call_grad2',
                       'pantalla_espera_grad1', 'pantalla_espera_grad2'),
        }),
        ('🖥️ Pantalla - Código de Turno', {
            'fields': ('pantalla_codigo_color', 'pantalla_codigo_fuente', 'pantalla_codigo_tamano'),
        }),
        ('🖥️ Pantalla - Nombre del Cliente', {
            'fields': ('pantalla_nombre_color', 'pantalla_nombre_fuente', 'pantalla_nombre_tamano'),
        }),
        ('🖥️ Pantalla - Mesa', {
            'fields': ('pantalla_mesa_color', 'pantalla_mesa_fuente', 'pantalla_mesa_tamano'),
        }),
        ('🖥️ Pantalla - Historial', {
            'fields': ('pantalla_historial_codigo', 'pantalla_historial_nombre', 'pantalla_historial_mesa'),
        }),
        ('🧭 Barra de Navegación', {
            'fields': ('nav_grad1', 'nav_grad2'),
        }),
        ('📱 Totem (Registro)', {
            'fields': ('totem_fondo_grad1', 'totem_fondo_grad2', 'totem_fondo_grad3',
                       'totem_header_grad1', 'totem_header_grad2'),
        }),
        ('🔘 Botones', {
            'fields': ('btn_llamar_grad1', 'btn_llamar_grad2',
                       'btn_completar_grad1', 'btn_completar_grad2',
                       'btn_guardar_grad1', 'btn_guardar_grad2'),
        }),
        ('📋 Turno Confirmado (Celular)', {
            'fields': ('confirmado_esperando_grad1', 'confirmado_esperando_grad2',
                       'confirmado_llamado_grad1', 'confirmado_llamado_grad2',
                       'confirmado_completado_grad1', 'confirmado_completado_grad2',
                       'confirmado_cancelado_grad1', 'confirmado_cancelado_grad2'),
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
