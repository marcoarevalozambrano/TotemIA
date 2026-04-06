"""
TotemIA v2.0 — Importar backup en un servidor MariaDB nuevo
Reconstruye completamente la base de datos desde un backup.

Uso:
  python importar_mariadb.py --sql backup_mariadb_20260401_120000.sql
  python importar_mariadb.py --sql backup.sql --media backup_media.zip
  python importar_mariadb.py --django-json backup_django.json
  python importar_mariadb.py --sql backup.sql --crear-bd  (crea la BD si no existe)

Opciones:
  --sql FILE          Archivo .sql generado por mysqldump
  --django-json FILE  Archivo .json generado por Django dumpdata (alternativa)
  --media FILE        Archivo .zip con los archivos media
  --crear-bd          Crear la base de datos si no existe (requiere root)
  --root-pass PASS    Contraseña de root para --crear-bd
"""
import os
import sys
import subprocess
import zipfile
import argparse
from pathlib import Path


def cargar_env():
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())


def encontrar_mysql():
    """Busca el cliente mysql local o detecta Docker."""
    import shutil

    # 1. Rutas conocidas en Windows
    for ruta in [
        r'C:\Program Files\MariaDB 11.8\bin\mysql.exe',
        r'C:\Program Files\MariaDB 11.7\bin\mysql.exe',
        r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe',
    ]:
        if Path(ruta).exists():
            return ('local', ruta)

    # 2. mysql en PATH (Linux/Mac/Windows)
    if shutil.which('mysql'):
        return ('local', 'mysql')

    # 3. Docker: buscar contenedor mariadb-totem
    if shutil.which('docker'):
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mariadb-totem', '--format', '{{.Names}}'],
            capture_output=True, text=True
        )
        if 'mariadb-totem' in result.stdout:
            return ('docker', 'mariadb-totem')

    # Fallback
    return ('local', 'mysql')


def main():
    parser = argparse.ArgumentParser(description='TotemIA — Importar MariaDB')
    parser.add_argument('--sql', help='Archivo .sql de backup')
    parser.add_argument('--django-json', help='Archivo .json de Django dumpdata')
    parser.add_argument('--media', help='Archivo .zip de media')
    parser.add_argument('--crear-bd', action='store_true', help='Crear BD si no existe')
    parser.add_argument('--root-pass', default='', help='Contraseña root para crear BD')
    args = parser.parse_args()

    if not args.sql and not args.django_json:
        parser.print_help()
        print("\n❌ Debe especificar --sql o --django-json")
        sys.exit(1)

    cargar_env()

    db_name = os.environ.get('DB_NAME', 'totem_ia')
    db_user = os.environ.get('DB_USER', 'totem')
    db_pass = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '3306')
    mysql_mode, mysql_ref = encontrar_mysql()

    print("╔══════════════════════════════════════════╗")
    print("║    TotemIA — Importar MariaDB            ║")
    print(f"║    BD: {db_name:<34}║")
    print(f"║    Host: {db_host:<32}║")
    print(f"║    Modo: {'Docker' if mysql_mode == 'docker' else 'Local':<32}║")
    print("╚══════════════════════════════════════════╝")
    print()

    # ── 1. Crear BD si se solicita ───────────────────────────
    if args.crear_bd:
        print("1. Creando base de datos y usuario...")
        root_pass = args.root_pass
        sql_setup = (
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; "
            f"CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_pass}'; "
            f"CREATE USER IF NOT EXISTS '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}'; "
            f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%'; "
            f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'localhost'; "
            f"FLUSH PRIVILEGES;"
        )
        if mysql_mode == 'docker':
            cmd = ['docker', 'exec', '-i', mysql_ref,
                   'mariadb', '-u', 'root', f'--password={root_pass}', '-e', sql_setup]
        else:
            cmd = [mysql_ref, f'--host={db_host}', f'--port={db_port}',
                   '-u', 'root', f'--password={root_pass}', '-e', sql_setup]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"   ❌ Error: {result.stderr[:300]}")
            sys.exit(1)
        print("   ✅ BD y usuario creados")
        print()

    # ── 2. Restaurar SQL ─────────────────────────────────────
    if args.sql:
        sql_file = Path(args.sql)
        if not sql_file.exists():
            print(f"❌ Archivo no encontrado: {sql_file}")
            sys.exit(1)

        print(f"2. Restaurando SQL desde {sql_file.name}...")
        size = sql_file.stat().st_size / 1024
        print(f"   Tamaño: {size:.1f} KB")

        if mysql_mode == 'docker':
            cmd = ['docker', 'exec', '-i', mysql_ref,
                   'mariadb',
                   f'--user={db_user}', f'--password={db_pass}',
                   '--default-character-set=utf8mb4',
                   db_name]
        else:
            cmd = [mysql_ref,
                   f'--host={db_host}', f'--port={db_port}',
                   f'--user={db_user}', f'--password={db_pass}',
                   '--default-character-set=utf8mb4',
                   db_name]

        with open(sql_file, 'r', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdin=f, capture_output=True, text=True, encoding='utf-8')

        if result.returncode != 0:
            print(f"   ❌ Error: {result.stderr[:300]}")
            sys.exit(1)
        print("   ✅ SQL restaurado")

    # ── 3. Restaurar Django JSON ─────────────────────────────
    if args.django_json:
        json_file = Path(args.django_json)
        if not json_file.exists():
            print(f"❌ Archivo no encontrado: {json_file}")
            sys.exit(1)

        print(f"2. Restaurando desde Django JSON: {json_file.name}...")
        os.environ['DB_ENGINE'] = 'mariadb'
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'totem_ia.settings')

        migrate_env = os.environ.copy()
        migrate_env['PYTHONIOENCODING'] = 'utf-8'

        # Primero migrar esquema
        print("   Aplicando migraciones...")
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--verbosity=1'],
            env=migrate_env, capture_output=True, text=True, encoding='utf-8'
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"   ❌ Error migraciones: {result.stderr[:300]}")
            sys.exit(1)

        # Luego cargar datos
        print("   Cargando datos...")
        result = subprocess.run(
            [sys.executable, 'manage.py', 'loaddata', str(json_file)],
            env=migrate_env, capture_output=True, text=True, encoding='utf-8'
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"   ❌ Error loaddata: {result.stderr[:300]}")
            sys.exit(1)
        print("   ✅ Datos restaurados")

    # ── 4. Restaurar Media ───────────────────────────────────
    if args.media:
        media_zip = Path(args.media)
        if not media_zip.exists():
            print(f"\n⚠ Archivo media no encontrado: {media_zip}")
        else:
            print(f"\n3. Restaurando media desde {media_zip.name}...")
            dest = Path(__file__).parent
            with zipfile.ZipFile(media_zip, 'r') as zf:
                zf.extractall(dest)
            print(f"   ✅ Media restaurada en {dest / 'media'}")

    print()
    print("✅ Importación completada.")
    print(f"   Iniciar servidor: python run_server.py --db mariadb")


if __name__ == '__main__':
    main()
