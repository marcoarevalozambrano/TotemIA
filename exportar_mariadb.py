"""
TotemIA v2.0 — Exportar base de datos MariaDB a backup completo
Genera:
  - backup_mariadb_YYYYMMDD_HHMMSS.sql  → dump SQL completo (estructura + datos)
  - backup_media_YYYYMMDD_HHMMSS.zip    → archivos subidos (logos, etc.)

Uso:
  python exportar_mariadb.py
  python exportar_mariadb.py --solo-sql     (sin media)
  python exportar_mariadb.py --solo-media   (sin SQL)
  python exportar_mariadb.py --output /ruta/destino
"""
import os
import sys
import subprocess
import zipfile
import argparse
from datetime import datetime
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

def main():
    parser = argparse.ArgumentParser(description='TotemIA — Exportar MariaDB')
    parser.add_argument('--solo-sql', action='store_true', help='Solo exportar SQL')
    parser.add_argument('--solo-media', action='store_true', help='Solo exportar archivos media')
    parser.add_argument('--output', default='.', help='Directorio de salida (default: .)')
    args = parser.parse_args()

    cargar_env()

    db_name = os.environ.get('DB_NAME', 'totem_ia')
    db_user = os.environ.get('DB_USER', 'totem')
    db_pass = os.environ.get('DB_PASSWORD', '')
    db_host = os.environ.get('DB_HOST', '127.0.0.1')
    db_port = os.environ.get('DB_PORT', '3306')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("╔══════════════════════════════════════════╗")
    print("║    TotemIA — Exportar MariaDB            ║")
    print(f"║    BD: {db_name:<34}║")
    print(f"║    Host: {db_host:<32}║")

    # Detectar modo: Docker o local
    import shutil
    mysql_mode = 'local'
    docker_container = 'mariadb-totem'

    if not shutil.which('mysqldump'):
        if shutil.which('docker'):
            result = subprocess.run(
                ['docker', 'ps', '--filter', f'name={docker_container}', '--format', '{{.Names}}'],
                capture_output=True, text=True
            )
            if docker_container in result.stdout:
                mysql_mode = 'docker'

    print(f"║    Modo: {'Docker' if mysql_mode == 'docker' else 'Local':<32}║")
    print("╚══════════════════════════════════════════╝")
    print()

    # ── 1. Dump SQL ──────────────────────────────────────────
    if not args.solo_media:
        sql_file = output_dir / f'backup_mariadb_{timestamp}.sql'
        print(f"1. Exportando SQL → {sql_file.name}")

        # Buscar mysqldump
        mysqldump = 'mysqldump'
        for ruta in [
            r'C:\Program Files\MariaDB 11.8\bin\mysqldump.exe',
            r'C:\Program Files\MariaDB 11.7\bin\mysqldump.exe',
            r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe',
        ]:
            if Path(ruta).exists():
                mysqldump = ruta
                break

        if mysql_mode == 'docker':
            cmd = [
                'docker', 'exec', docker_container,
                'mariadb-dump',
                f'--user={db_user}',
                f'--password={db_pass}',
                '--single-transaction',
                '--routines',
                '--triggers',
                '--add-drop-table',
                '--create-options',
                '--default-character-set=utf8mb4',
                db_name,
            ]
        else:
            cmd = [
                mysqldump,
                f'--host={db_host}',
                f'--port={db_port}',
                f'--user={db_user}',
                f'--password={db_pass}',
                '--single-transaction',
                '--routines',
                '--triggers',
                '--add-drop-table',
                '--create-options',
                '--default-character-set=utf8mb4',
                db_name,
            ]

        try:
            with open(sql_file, 'w', encoding='utf-8') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            if result.returncode != 0:
                print(f"   ⚠ Advertencia mysqldump: {result.stderr[:200]}")
            size = sql_file.stat().st_size / 1024
            print(f"   ✅ {sql_file.name} ({size:.1f} KB)")
        except FileNotFoundError:
            print(f"   ❌ mysqldump no encontrado. Usando Django dumpdata como alternativa...")
            _dump_django(output_dir, timestamp)

    # ── 2. Media ZIP ─────────────────────────────────────────
    if not args.solo_sql:
        media_dir = Path(__file__).parent / 'media'
        if media_dir.exists() and any(media_dir.rglob('*')):
            zip_file = output_dir / f'backup_media_{timestamp}.zip'
            print(f"\n2. Exportando media → {zip_file.name}")
            with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for archivo in media_dir.rglob('*'):
                    if archivo.is_file():
                        zf.write(archivo, archivo.relative_to(media_dir.parent))
            size = zip_file.stat().st_size / 1024
            print(f"   ✅ {zip_file.name} ({size:.1f} KB)")
        else:
            print(f"\n2. Media: directorio vacío o inexistente, omitiendo.")

    print()
    print("✅ Exportación completada.")
    print(f"   Archivos en: {output_dir.resolve()}")
    print()
    print("Para restaurar en otro servidor:")
    print(f"   python importar_mariadb.py --sql {output_dir}/backup_mariadb_{timestamp}.sql")


def _dump_django(output_dir, timestamp):
    """Fallback: usar Django dumpdata si mysqldump no está disponible"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'totem_ia.settings')
    os.environ['DB_ENGINE'] = 'mariadb'
    import django
    django.setup()
    from django.core.management import call_command
    json_file = output_dir / f'backup_django_{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        call_command('dumpdata',
                     '--natural-foreign', '--natural-primary',
                     '--exclude=contenttypes', '--exclude=auth.permission',
                     '--exclude=sessions.session',
                     '--indent=2', stdout=f)
    size = json_file.stat().st_size / 1024
    print(f"   ✅ {json_file.name} ({size:.1f} KB) [formato Django JSON]")
    print(f"   ℹ Para restaurar usar: python importar_mariadb.py --django-json {json_file}")


if __name__ == '__main__':
    main()
