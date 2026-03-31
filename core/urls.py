from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Interfaz 1: Totem (registro de cliente)
    path('', views.totem_view, name='totem'),
    path('api/registrar-turno/', views.registrar_turno, name='registrar_turno'),
    path('turno-confirmado/<int:turno_id>/', views.turno_confirmado, name='turno_confirmado'),

    # Interfaz 2: Pantalla de visualización
    path('pantalla/', views.pantalla_view, name='pantalla'),
    path('api/turnos-activos/', views.turnos_activos, name='turnos_activos'),
    path('api/logos-pantalla/', views.logos_pantalla, name='logos_pantalla'),
    path('api/videos-pantalla/', views.videos_pantalla, name='videos_pantalla'),
    path('api/apariencia/', views.api_apariencia, name='api_apariencia'),

    # Interfaz 3: Mesa de atención
    path('mesa/', views.mesa_view, name='mesa'),
    path('api/llamar-turno/', views.llamar_turno, name='llamar_turno'),
    path('api/rellamar-turno/', views.rellamar_turno, name='rellamar_turno'),
    path('api/completar-turno/', views.completar_turno, name='completar_turno'),
    path('api/actualizar-cliente/', views.actualizar_cliente, name='actualizar_cliente'),
    path('api/turnos-espera/', views.turnos_espera, name='turnos_espera'),
    path('api/turno-actual/', views.turno_actual, name='turno_actual'),
    path('api/estado-turno/<int:turno_id>/', views.estado_turno, name='estado_turno'),
    path('api/toggle-preferencial/', views.toggle_preferencial, name='toggle_preferencial'),

    # Admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/login/', views.login_view, name='login'),
    path('admin-panel/logout/', views.logout_view, name='logout'),
    path('admin-panel/exportar-excel/', views.exportar_excel, name='exportar_excel'),
    path('admin-panel/logs/', views.ver_logs, name='ver_logs'),
    path('api/mis-estadisticas/', views.api_mis_estadisticas, name='mis_estadisticas'),
]
