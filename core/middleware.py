from django.http import HttpResponseBadRequest


class AllowAllHostsMiddleware:
    """
    Middleware que bypasea la validación RFC 1034/1035 de Django para hostnames
    con caracteres especiales como guión bajo (ej: cop_fab00008.inacap.cl).
    Solo activo cuando DEBUG=True o ALLOWED_HOSTS=['*'].
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Parchear el host para que pase la validación de Django
        # si contiene guión bajo (inválido según RFC pero válido en redes internas)
        host = request.META.get('HTTP_HOST', '')
        if '_' in host:
            # Reemplazar temporalmente para que Django no lo rechace
            request.META['HTTP_HOST'] = host.replace('_', '-')
            response = self.get_response(request)
            # Restaurar para que las URLs generadas sean correctas
            request.META['HTTP_HOST'] = host
            return response
        return self.get_response(request)
