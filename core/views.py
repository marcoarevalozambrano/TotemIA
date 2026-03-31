import json
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from openpyxl import Workbook
from .models import Cliente, Turno, Mesa, LogAtencion, LogoPantalla, MarquesinaPantalla, VideoPantalla, ConfigVideoPantalla, ConfigApariencia


# ============================================================
# INTERFAZ 1: TOTEM - Registro de clientes
# ============================================================

def totem_view(request):
    """Pantalla del totem para registro de clientes"""
    return render(request, 'core/totem.html')


@csrf_exempt
@require_POST
def registrar_turno(request):
    """API para registrar un nuevo turno"""
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre_completo', '').strip()
        rut = data.get('rut', '').strip()
        fecha_nac = data.get('fecha_nacimiento', '')
        telefono = data.get('telefono', '').strip()
        email = data.get('email', '').strip()

        if not nombre or not telefono:
            return JsonResponse({'error': 'Nombre y teléfono son obligatorios'}, status=400)

        fecha_obj = None
        if fecha_nac:
            try:
                fecha_obj = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
            except ValueError:
                fecha_obj = None

        cliente = Cliente.objects.create(
            nombre_completo=nombre,
            rut=rut,
            fecha_nacimiento=fecha_obj,
            telefono=telefono,
            email=email,
        )

        # Determinar si es preferencial (tercera edad o solicitud manual)
        es_preferencial = False
        motivo = ''
        solicita_preferencial = data.get('solicita_preferencial', False)

        if solicita_preferencial:
            es_preferencial = True
            motivo = 'solicitud'

        if fecha_obj:
            from datetime import date
            hoy = date.today()
            edad = hoy.year - fecha_obj.year - ((hoy.month, hoy.day) < (fecha_obj.month, fecha_obj.day))
            if edad >= 60:
                es_preferencial = True
                motivo = 'edad' if not solicita_preferencial else 'edad+solicitud'

        turno = Turno.objects.create(
            codigo=Turno.generar_codigo(),
            cliente=cliente,
            es_preferencial=es_preferencial,
            motivo_preferencial=motivo,
        )

        return JsonResponse({
            'success': True,
            'turno_id': turno.id,
            'codigo': turno.codigo,
            'nombre': cliente.nombre_completo,
            'es_preferencial': es_preferencial,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def turno_confirmado(request, turno_id):
    """Pantalla de confirmación del turno"""
    turno = get_object_or_404(Turno, id=turno_id)
    return render(request, 'core/turno_confirmado.html', {'turno': turno})


# ============================================================
# INTERFAZ 2: PANTALLA DE VISUALIZACIÓN
# ============================================================

def pantalla_view(request):
    """Pantalla grande de visualización de llamados"""
    return render(request, 'core/pantalla.html')


def turnos_activos(request):
    """API: turnos llamados/atendiendo para la pantalla"""
    hoy = timezone.now().date()
    actual = Turno.objects.filter(
        estado='llamado',
        llamado_en__date=hoy
    ).select_related('cliente', 'mesa').order_by('-llamado_en').first()

    historial = Turno.objects.filter(
        estado__in=['atendiendo', 'completado', 'cancelado'],
        llamado_en__date=hoy
    ).select_related('cliente', 'mesa').order_by('-llamado_en')[:5]

    en_espera = Turno.objects.filter(
        estado='esperando',
        creado_en__date=hoy
    ).count()

    data = {
        'actual': None,
        'historial': [],
        'en_espera': en_espera,
    }

    if actual:
        data['actual'] = {
            'codigo': actual.codigo,
            'nombre': actual.cliente.nombre_completo,
            'mesa': actual.mesa.nombre if actual.mesa else '',
            'es_preferencial': actual.es_preferencial,
            'llamado_en': actual.llamado_en.isoformat() if actual.llamado_en else '',
        }

    for t in historial:
        data['historial'].append({
            'codigo': t.codigo,
            'nombre': t.cliente.nombre_completo,
            'mesa': t.mesa.nombre if t.mesa else '',
            'estado': t.estado,
            'es_preferencial': t.es_preferencial,
        })

    return JsonResponse(data)


def logos_pantalla(request):
    """API: logos y marquesina activos para la pantalla de llamado"""
    logos = LogoPantalla.objects.filter(activo=True)
    logos_data = [{'nombre': l.nombre, 'url': l.imagen.url} for l in logos]

    marquesinas_data = []
    marquesinas = MarquesinaPantalla.objects.filter(activo=True)
    for m in marquesinas:
        marquesinas_data.append({
            'texto': m.texto,
            'color': m.color,
            'velocidad': m.velocidad,
            'tamano_fuente': m.tamano_fuente,
        })

    return JsonResponse({'logos': logos_data, 'marquesinas': marquesinas_data})


def _get_embed_url(url):
    """Convierte URL de YouTube/Vimeo a URL embebible"""
    import re
    # YouTube
    yt = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})', url)
    if yt:
        return f'https://www.youtube.com/embed/{yt.group(1)}?autoplay=1&mute=0&enablejsapi=1&loop=0&controls=0&modestbranding=1&rel=0'
    # Vimeo
    vm = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
    if vm:
        return f'https://player.vimeo.com/video/{vm.group(1)}?autoplay=1&muted=0&loop=0&background=0&api=1'
    return url


def videos_pantalla(request):
    """API: videos y config para el reproductor de la pantalla"""
    config = ConfigVideoPantalla.objects.first()
    if not config or not config.habilitado:
        return JsonResponse({'habilitado': False, 'videos': []})

    videos = list(VideoPantalla.objects.filter(activo=True).values('titulo', 'url', 'orden'))

    # Extraer embed URLs
    import re
    for v in videos:
        v['embed_url'] = _get_embed_url(v['url'])

    return JsonResponse({
        'habilitado': True,
        'modo': config.modo_reproduccion,
        'volumen': config.volumen,
        'videos': videos,
    })


def api_apariencia(request):
    """API: configuración de apariencia (colores y tipografía)"""
    conf = ConfigApariencia.objects.first()
    if not conf:
        conf = ConfigApariencia()  # Usa defaults sin guardar
    # Serializar todos los campos excepto id
    data = {}
    for f in conf._meta.get_fields():
        if f.name == 'id':
            continue
        data[f.name] = getattr(conf, f.name)
    return JsonResponse(data)


# ============================================================
# INTERFAZ 3: MESA DE ATENCIÓN
# ============================================================

@login_required
def mesa_view(request):
    """Interfaz de la mesa de atención"""
    mesas = Mesa.objects.filter(activa=True)
    return render(request, 'core/mesa.html', {'mesas': mesas, 'es_admin': request.user.is_superuser})


@csrf_exempt
@require_POST
def llamar_turno(request):
    """API: llamar al siguiente turno"""
    try:
        data = json.loads(request.body)
        mesa_id = data.get('mesa_id')
        mesa = get_object_or_404(Mesa, id=mesa_id)

        # Cancelar turnos anteriores de esta mesa (llamados o atendiendo)
        turnos_anteriores = Turno.objects.filter(mesa=mesa, estado__in=['llamado', 'atendiendo'])
        for t in turnos_anteriores:
            t.estado = 'cancelado'
            t.completado_en = timezone.now()
            t.save()
            LogAtencion.objects.create(
                turno=t,
                usuario=request.user if request.user.is_authenticated else None,
                accion='cancelado',
                detalle=f'Turno cancelado al llamar siguiente en mesa {mesa.nombre}'
            )

        # Tomar el siguiente en espera
        # Si la mesa es preferencial, priorizar clientes de tercera edad
        turnos_hoy = Turno.objects.filter(
            estado='esperando',
            creado_en__date=timezone.now().date()
        )

        siguiente = None
        if mesa.preferencial:
            # Primero buscar preferenciales (tercera edad) por orden de llegada
            siguiente = turnos_hoy.filter(
                es_preferencial=True
            ).order_by('creado_en').first()

        # Si no hay preferenciales o la mesa no es preferencial, tomar el siguiente normal
        if not siguiente:
            siguiente = turnos_hoy.order_by('creado_en').first()

        if not siguiente:
            return JsonResponse({'error': 'No hay turnos en espera'}, status=404)

        siguiente.estado = 'llamado'
        siguiente.mesa = mesa
        siguiente.atendido_por = request.user if request.user.is_authenticated else None
        siguiente.llamado_en = timezone.now()
        siguiente.save()

        LogAtencion.objects.create(
            turno=siguiente,
            usuario=request.user if request.user.is_authenticated else None,
            accion='llamado',
            detalle=f'Llamado a mesa {mesa.nombre}'
        )

        return JsonResponse({
            'success': True,
            'turno': {
                'id': siguiente.id,
                'codigo': siguiente.codigo,
                'nombre': siguiente.cliente.nombre_completo,
                'rut': siguiente.cliente.rut,
                'telefono': siguiente.cliente.telefono,
                'email': siguiente.cliente.email,
                'fecha_nacimiento': str(siguiente.cliente.fecha_nacimiento) if siguiente.cliente.fecha_nacimiento else '',
                'observaciones': siguiente.cliente.observaciones,
                'es_preferencial': siguiente.es_preferencial,
                'motivo_preferencial': siguiente.motivo_preferencial,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def rellamar_turno(request):
    """API: volver a llamar al turno actual (re-trigger en pantalla y celular)"""
    try:
        data = json.loads(request.body)
        turno_id = data.get('turno_id')
        turno = get_object_or_404(Turno, id=turno_id)
        turno.estado = 'llamado'
        turno.llamado_en = timezone.now()
        turno.save()

        LogAtencion.objects.create(
            turno=turno,
            usuario=request.user if request.user.is_authenticated else None,
            accion='rellamado',
            detalle=f'Turno rellamado en mesa {turno.mesa.nombre if turno.mesa else "N/A"}'
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def completar_turno(request):
    """API: marcar turno como completado"""
    try:
        data = json.loads(request.body)
        turno_id = data.get('turno_id')
        turno = get_object_or_404(Turno, id=turno_id)
        turno.estado = 'completado'
        turno.completado_en = timezone.now()
        turno.save()

        LogAtencion.objects.create(
            turno=turno,
            usuario=request.user if request.user.is_authenticated else None,
            accion='completado',
            detalle=f'Atención completada en mesa {turno.mesa.nombre if turno.mesa else "N/A"}'
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
def actualizar_cliente(request):
    """API: actualizar datos del cliente desde la mesa"""
    try:
        data = json.loads(request.body)
        turno_id = data.get('turno_id')
        turno = get_object_or_404(Turno, id=turno_id)
        cliente = turno.cliente

        if 'nombre_completo' in data:
            cliente.nombre_completo = data['nombre_completo']
        if 'rut' in data:
            cliente.rut = data['rut']
        if 'telefono' in data:
            cliente.telefono = data['telefono']
        if 'email' in data:
            cliente.email = data['email']
        if 'observaciones' in data:
            cliente.observaciones = data['observaciones']
        if 'fecha_nacimiento' in data and data['fecha_nacimiento']:
            try:
                cliente.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()
            except ValueError:
                pass

        cliente.save()

        LogAtencion.objects.create(
            turno=turno,
            usuario=request.user if request.user.is_authenticated else None,
            accion='datos_actualizados',
            detalle='Datos del cliente actualizados desde mesa'
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def turnos_espera(request):
    """API: lista de turnos en espera, paginada, con orden preferencial"""
    hoy = timezone.now().date()
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))
    mesa_id = request.GET.get('mesa_id', '')

    queryset = Turno.objects.filter(
        estado='esperando', creado_en__date=hoy
    ).select_related('cliente')

    total = queryset.count()
    total_pref = queryset.filter(es_preferencial=True).count()

    # Si la mesa es preferencial, ordenar preferenciales primero
    es_mesa_pref = False
    if mesa_id:
        try:
            mesa = Mesa.objects.get(id=mesa_id)
            es_mesa_pref = mesa.preferencial
        except Mesa.DoesNotExist:
            pass

    if es_mesa_pref:
        from django.db.models import Case, When, IntegerField
        queryset = queryset.annotate(
            prioridad=Case(
                When(es_preferencial=True, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).order_by('prioridad', 'creado_en')
    else:
        queryset = queryset.order_by('creado_en')

    turnos = queryset[offset:offset + limit]

    data = [{
        'id': t.id,
        'codigo': t.codigo,
        'nombre': t.cliente.nombre_completo,
        'creado_en': timezone.localtime(t.creado_en).strftime('%H:%M'),
        'es_preferencial': t.es_preferencial,
        'motivo_preferencial': t.motivo_preferencial,
    } for t in turnos]

    return JsonResponse({
        'turnos': data,
        'total': total,
        'total_pref': total_pref,
        'offset': offset,
        'has_more': (offset + limit) < total,
        'mesa_preferencial': es_mesa_pref,
    })


def turno_actual(request):
    """API: turno actualmente siendo atendido en una mesa"""
    mesa_id = request.GET.get('mesa_id')
    if not mesa_id:
        return JsonResponse({'error': 'mesa_id requerido'}, status=400)

    turno = Turno.objects.filter(
        mesa_id=mesa_id,
        estado__in=['llamado', 'atendiendo']
    ).select_related('cliente').order_by('-llamado_en').first()

    if not turno:
        return JsonResponse({'turno': None})

    return JsonResponse({
        'turno': {
            'id': turno.id,
            'codigo': turno.codigo,
            'nombre': turno.cliente.nombre_completo,
            'rut': turno.cliente.rut,
            'telefono': turno.cliente.telefono,
            'email': turno.cliente.email,
            'fecha_nacimiento': str(turno.cliente.fecha_nacimiento) if turno.cliente.fecha_nacimiento else '',
            'observaciones': turno.cliente.observaciones,
            'es_preferencial': turno.es_preferencial,
        }
    })


def estado_turno(request, turno_id):
    """API: estado actual de un turno (para notificar al cliente en su celular)"""
    turno = get_object_or_404(Turno, id=turno_id)
    return JsonResponse({
        'codigo': turno.codigo,
        'estado': turno.estado,
        'mesa': turno.mesa.nombre if turno.mesa else '',
        'es_preferencial': turno.es_preferencial,
    })


@csrf_exempt
@require_POST
def toggle_preferencial(request):
    """API: activar/desactivar modo preferencial de una mesa"""
    try:
        data = json.loads(request.body)
        mesa_id = data.get('mesa_id')
        preferencial = data.get('preferencial', False)
        mesa = get_object_or_404(Mesa, id=mesa_id)
        mesa.preferencial = preferencial
        mesa.save()
        return JsonResponse({'success': True, 'preferencial': mesa.preferencial})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================
# ADMIN PANEL
# ============================================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('core:admin_panel')
        return render(request, 'core/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:login')


@login_required
def admin_panel(request):
    """Panel: admin ve todo, operador ve solo sus métricas"""
    hoy = timezone.now().date()
    turnos_hoy = Turno.objects.filter(creado_en__date=hoy).select_related('cliente', 'mesa', 'atendido_por')
    total_espera = turnos_hoy.filter(estado='esperando').count()
    total_atendidos = turnos_hoy.filter(estado='completado').count()
    total_hoy = turnos_hoy.count()

    context = {
        'total_espera': total_espera,
        'total_atendidos': total_atendidos,
        'total_hoy': total_hoy,
        'es_admin': request.user.is_superuser,
    }

    if request.user.is_superuser:
        context['turnos'] = turnos_hoy
        context['mesas'] = Mesa.objects.all()

    return render(request, 'core/admin_panel.html', context)


@login_required
def exportar_excel(request):
    """Exportar datos a Excel - solo admin"""
    if not request.user.is_superuser:
        return HttpResponse('No autorizado', status=403)

    wb = Workbook()
    ws = wb.active
    ws.title = "Turnos"

    headers = ['Código', 'RUT', 'Nombre', 'Teléfono', 'Email', 'F. Nacimiento',
               'Preferencial', 'Motivo', 'Estado', 'Mesa', 'Atendido por', 'Observaciones',
               'Creado', 'Llamado', 'Completado']
    ws.append(headers)

    turnos = Turno.objects.all().select_related('cliente', 'mesa', 'atendido_por').order_by('-creado_en')

    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')
    if fecha_desde:
        turnos = turnos.filter(creado_en__date__gte=fecha_desde)
    if fecha_hasta:
        turnos = turnos.filter(creado_en__date__lte=fecha_hasta)

    for t in turnos:
        ws.append([
            t.codigo,
            t.cliente.rut,
            t.cliente.nombre_completo,
            t.cliente.telefono,
            t.cliente.email,
            str(t.cliente.fecha_nacimiento) if t.cliente.fecha_nacimiento else '',
            'Sí' if t.es_preferencial else 'No',
            t.motivo_preferencial or '',
            t.get_estado_display(),
            t.mesa.nombre if t.mesa else '',
            t.atendido_por.get_full_name() if t.atendido_por else '',
            t.cliente.observaciones,
            t.creado_en.strftime('%Y-%m-%d %H:%M'),
            t.llamado_en.strftime('%Y-%m-%d %H:%M') if t.llamado_en else '',
            t.completado_en.strftime('%Y-%m-%d %H:%M') if t.completado_en else '',
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=totem_ia_turnos.xlsx'
    wb.save(response)
    return response


@login_required
def ver_logs(request):
    """Ver logs de auditoría - solo admin"""
    if not request.user.is_superuser:
        return HttpResponse('No autorizado', status=403)
    logs = LogAtencion.objects.all().select_related('turno', 'usuario').order_by('-timestamp')[:200]
    return render(request, 'core/logs.html', {'logs': logs})


@login_required
def api_mis_estadisticas(request):
    """API: estadísticas de la jornada diaria actual"""
    usuario = request.user
    hoy = timezone.now().date()
    ahora = timezone.now()

    # Todos los turnos del día
    turnos_dia = Turno.objects.filter(creado_en__date=hoy).select_related('mesa', 'cliente')

    # Mis turnos (operador actual)
    mis_turnos = turnos_dia.filter(atendido_por=usuario)
    mis_completados = mis_turnos.filter(estado='completado')
    mis_cancelados = mis_turnos.filter(estado='cancelado')

    # Tiempo promedio de atención (mis completados)
    tiempos = []
    for t in mis_completados.filter(llamado_en__isnull=False, completado_en__isnull=False):
        delta = (t.completado_en - t.llamado_en).total_seconds()
        if delta > 0:
            tiempos.append(delta)
    mi_promedio = sum(tiempos) / len(tiempos) if tiempos else 0

    # Tiempo promedio global del día
    tiempos_global = []
    for t in turnos_dia.filter(estado='completado', llamado_en__isnull=False, completado_en__isnull=False):
        delta = (t.completado_en - t.llamado_en).total_seconds()
        if delta > 0:
            tiempos_global.append(delta)
    promedio_global = sum(tiempos_global) / len(tiempos_global) if tiempos_global else 0

    # Flujo por hora del día (todos los turnos creados)
    flujo_hora = {}
    for t in turnos_dia:
        h = t.creado_en.hour
        flujo_hora[h] = flujo_hora.get(h, 0) + 1
    # Atendidos por hora (completados)
    atendidos_hora = {}
    for t in turnos_dia.filter(estado='completado', completado_en__isnull=False):
        h = t.completado_en.hour
        atendidos_hora[h] = atendidos_hora.get(h, 0) + 1
    # Rango de horas del día
    todas_horas = sorted(set(list(flujo_hora.keys()) + list(atendidos_hora.keys())))
    if not todas_horas:
        todas_horas = [ahora.hour]
    flujo_labels = [f'{h:02d}:00' for h in todas_horas]
    flujo_ingresados = [flujo_hora.get(h, 0) for h in todas_horas]
    flujo_completados = [atendidos_hora.get(h, 0) for h in todas_horas]

    # Estado actual por mesa (snapshot de la jornada)
    mesas = Mesa.objects.filter(activa=True)
    mesas_data = []
    for mesa in mesas:
        turnos_mesa = turnos_dia.filter(mesa=mesa)
        completados_mesa = turnos_mesa.filter(estado='completado').count()
        cancelados_mesa = turnos_mesa.filter(estado='cancelado').count()
        en_atencion = turnos_mesa.filter(estado__in=['llamado', 'atendiendo']).first()
        # Promedio de esta mesa
        t_mesa = []
        for t in turnos_mesa.filter(estado='completado', llamado_en__isnull=False, completado_en__isnull=False):
            delta = (t.completado_en - t.llamado_en).total_seconds()
            if delta > 0:
                t_mesa.append(delta)
        prom_mesa = sum(t_mesa) / len(t_mesa) if t_mesa else 0

        mesas_data.append({
            'nombre': mesa.nombre,
            'preferencial': mesa.preferencial,
            'completados': completados_mesa,
            'cancelados': cancelados_mesa,
            'promedio_min': round(prom_mesa / 60, 1),
            'turno_actual': en_atencion.codigo if en_atencion else None,
            'operador': en_atencion.atendido_por.get_full_name() or en_atencion.atendido_por.username if en_atencion and en_atencion.atendido_por else '-',
        })

    # Preferenciales vs normales del día (global)
    pref_dia = turnos_dia.filter(es_preferencial=True).count()
    normal_dia = turnos_dia.filter(es_preferencial=False).count()

    # Espera actual
    en_espera = turnos_dia.filter(estado='esperando').count()
    # Tiempo promedio de espera (desde creado hasta llamado, de los ya llamados hoy)
    esperas = []
    for t in turnos_dia.filter(llamado_en__isnull=False):
        delta = (t.llamado_en - t.creado_en).total_seconds()
        if delta > 0:
            esperas.append(delta)
    promedio_espera = sum(esperas) / len(esperas) if esperas else 0

    return JsonResponse({
        # Mis indicadores
        'mis_completados': mis_completados.count(),
        'mis_cancelados': mis_cancelados.count(),
        'mis_total': mis_turnos.count(),
        'mi_promedio_min': round(mi_promedio / 60, 1),
        # Indicadores globales del día
        'total_dia': turnos_dia.count(),
        'completados_dia': turnos_dia.filter(estado='completado').count(),
        'en_espera': en_espera,
        'promedio_global_min': round(promedio_global / 60, 1),
        'promedio_espera_min': round(promedio_espera / 60, 1),
        # Flujo por hora
        'flujo': {
            'labels': flujo_labels,
            'ingresados': flujo_ingresados,
            'completados': flujo_completados,
        },
        # Mesas
        'mesas': mesas_data,
        # Preferenciales
        'preferenciales': {'pref': pref_dia, 'normal': normal_dia},
    })
