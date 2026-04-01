"""
TotemIA v2.0 — Launcher con selección de base de datos
Uso:
  python run_server.py                  → SQLite (default)
  python run_server.py --db mariadb     → MariaDB
  python run_server.py --db sqlite      → SQLite explícito
  python run_server.py --db mariadb --migrate  → MariaDB + migrar
"""
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='TotemIA Server Launcher')
    parser.add_argument('--db', choices=['sqlite', 'mariadb'], default='sqlite',
                        help='Motor de base de datos (default: sqlite)')
    parser.add_argument('--migrate', action='store_true',
                        help='Ejecutar migraciones antes de iniciar')
    parser.add_argument('--https', action='store_true',
                        help='Iniciar con HTTPS (puerto 8443)')
    parser.add_argument('--port', type=int, default=None,
                        help='Puerto personalizado')
    args = parser.parse_args()

    # Configurar motor de BD
    os.environ['DB_ENGINE'] = args.db
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'totem_ia.settings')

    print(f"╔══════════════════════════════════════╗")
    print(f"║        TotemIA v2.0 Launcher         ║")
    print(f"╠══════════════════════════════════════╣")
    print(f"║  Base de datos: {args.db.upper():>18}  ║")

    if args.db == 'mariadb':
        # Cargar .env si existe
        env_file = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        os.environ.setdefault(key.strip(), val.strip())
            print(f"║  Host: {os.environ.get('DB_HOST', '127.0.0.1'):>27}  ║")
            print(f"║  BD:   {os.environ.get('DB_NAME', 'totem_ia'):>27}  ║")
        else:
            print(f"║  ⚠ Sin .env — usando defaults        ║")
            print(f"║  Copie .env.example a .env            ║")

    print(f"╚══════════════════════════════════════╝")
    print()

    import django
    django.setup()

    if args.migrate:
        print("→ Ejecutando migraciones...")
        from django.core.management import call_command
        call_command('migrate', verbosity=1)
        print()

    if args.https:
        port = args.port or 8443
        print(f"→ Iniciando HTTPS en 0.0.0.0:{port}...")
        import ssl
        from django.core.wsgi import get_wsgi_application
        from django.contrib.staticfiles.handlers import StaticFilesHandler
        from django.conf import settings
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import mimetypes

        class QuietHandler(WSGIRequestHandler):
            def log_message(self, format, *args):
                sys.stderr.write(f"[HTTPS] {args[0]} {args[1]} {args[2]}\n")

        class MediaHandler:
            def __init__(self, app):
                self.app = app
                self.media_url = settings.MEDIA_URL
                self.media_root = str(settings.MEDIA_ROOT)
            def __call__(self, environ, start_response):
                path = environ.get('PATH_INFO', '/')
                if path.startswith(self.media_url):
                    rel = path[len(self.media_url):]
                    fp = os.path.join(self.media_root, rel.replace('/', os.sep))
                    if os.path.isfile(fp):
                        ct, _ = mimetypes.guess_type(fp)
                        ct = ct or 'application/octet-stream'
                        with open(fp, 'rb') as f:
                            data = f.read()
                        start_response('200 OK', [('Content-Type', ct), ('Content-Length', str(len(data)))])
                        return [data]
                return self.app(environ, start_response)

        app = MediaHandler(StaticFilesHandler(get_wsgi_application()))
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain('cert.pem', 'key.pem')
        server = make_server('0.0.0.0', port, app, handler_class=QuietHandler)
        server.socket = ctx.wrap_socket(server.socket, server_side=True)
        print(f"   https://0.0.0.0:{port}/")
        server.serve_forever()
    else:
        port = args.port or 8000
        print(f"→ Iniciando HTTP en 0.0.0.0:{port}...")
        from django.core.management import call_command
        call_command('runserver', f'0.0.0.0:{port}')

if __name__ == '__main__':
    main()
