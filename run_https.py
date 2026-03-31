"""Servidor HTTPS para desarrollo de TotemIA"""
import os
import ssl
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'totem_ia.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.conf import settings
from wsgiref.simple_server import make_server, WSGIRequestHandler
import mimetypes
import posixpath

class QuietHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[HTTPS] {args[0]} {args[1]} {args[2]}\n")

class MediaStaticHandler:
    """Sirve archivos de /media/ además de los estáticos de Django"""
    def __init__(self, app):
        self.app = app
        self.media_url = settings.MEDIA_URL
        self.media_root = str(settings.MEDIA_ROOT)

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        if path.startswith(self.media_url):
            rel_path = path[len(self.media_url):]
            file_path = os.path.join(self.media_root, rel_path.replace('/', os.sep))
            if os.path.isfile(file_path):
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or 'application/octet-stream'
                with open(file_path, 'rb') as f:
                    data = f.read()
                start_response('200 OK', [
                    ('Content-Type', content_type),
                    ('Content-Length', str(len(data))),
                ])
                return [data]
        return self.app(environ, start_response)

application = MediaStaticHandler(StaticFilesHandler(get_wsgi_application()))

host = '0.0.0.0'
port = 8443

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('cert.pem', 'key.pem')

server = make_server(host, port, application, handler_class=QuietHandler)
server.socket = ctx.wrap_socket(server.socket, server_side=True)

print(f"TotemIA HTTPS corriendo en https://{host}:{port}/")
print(f"Desde tu teléfono: https://10.10.48.33:{port}/")
print("(Acepta el certificado autofirmado en el navegador)")

server.serve_forever()
