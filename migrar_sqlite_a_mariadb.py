"""
TotemIA v2.0 — Migrar datos de SQLite a MariaDB
Uso:
  1. Configurar .env con los datos de MariaDB
  2. Crear la BD en MariaDB: CREATE DATABASE totem_ia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  3. Ejecutar: python migrar_sqlite_a_mariadb.py

Este script:
  - Exporta datos de SQLite a un fixture JSON
  - Aplica migraciones en MariaDB
  - Importa los datos en MariaDB
"""
import os
import sys
import subprocess

def run(cmd, env=None):
    """Ejecutar comando y mostrar salida"""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, env=full_env, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        return False
    return True

def main():
    print("╔══════════════════════════════════════════╗")
    print("║  TotemIA — Migración SQLite → MariaDB    ║")
    print("╚══════════════════════════════════════════╝")
    print()

    # Cargar .env
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ[key.strip()] = val.strip()

    # Paso 1: Exportar datos desde SQLite
    print("1. Exportando datos desde SQLite...")
    if not run('python manage.py dumpdata --natural-foreign --natural-primary --exclude=contenttypes --exclude=auth.permission --indent=2 -o fixture_backup.json',
               env={'DB_ENGINE': 'sqlite'}):
        print("   Fallo al exportar. ¿Existe db.sqlite3?")
        return

    print()
    print("2. Aplicando migraciones en MariaDB...")
    if not run('python manage.py migrate', env={'DB_ENGINE': 'mariadb'}):
        print("   Fallo al migrar. Verifique conexión a MariaDB y .env")
        return

    print()
    print("3. Importando datos en MariaDB...")
    if not run('python manage.py loaddata fixture_backup.json', env={'DB_ENGINE': 'mariadb'}):
        print("   Fallo al importar. Revise el fixture.")
        return

    print()
    print("✅ Migración completada exitosamente.")
    print("   Puede iniciar con: python run_server.py --db mariadb")
    print("   El archivo fixture_backup.json puede eliminarse.")

if __name__ == '__main__':
    main()
