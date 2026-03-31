"""Script para cargar usuarios desde la lista proporcionada"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'totem_ia.settings')
django.setup()

from django.contrib.auth.models import User

USUARIOS = [
    ("SARA MURA", "smura"),
    ("Emily Alcalá", "ealcala"),
    ("BENJAMIN MORALES", "bmorales"),
    ("SOFIA VALENZUELA", "svalenzuela"),
    ("Aylin Rojas", "arojas"),
    ("ALMENDRA FUENTES", "afuentes"),
    ("Lissette Pizarro", "lpizarro"),
    ("SOFIA AVALOS", "savalos"),
    ("ANTONELLA GOMEZ", "agomez"),
    ("JEAN ASTUDILLO", "jastudillo"),
    ("GERMAN CUELLAR", "gcuellar"),
    ("AMANDA GALLEGUILLOS", "agalleguillos"),
    ("MAYRA ARANDA", "maranda"),
    ("Lissette Araya", "laraya"),
    ("Ignacia Díaz Cruz", "idiaz"),
    ("Isidora Jaque", "ijaque"),
    ("Javiera Valenzuela", "jvalenzuela"),
    ("Nair Medina", "nmedina"),
    ("Escarlen Jimenez", "ejimenez"),
    ("Constanza Avila", "cavila"),
]

PASSWORD = "Inacap2026"

for nombre_completo, username in USUARIOS:
    partes = nombre_completo.strip().split()
    first_name = partes[0].title() if partes else ""
    last_name = " ".join(partes[1:]).title() if len(partes) > 1 else ""

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'is_staff': True,
        }
    )
    if created:
        user.set_password(PASSWORD)
        user.save()
        print(f"  + {username} ({first_name} {last_name})")
    else:
        print(f"  = {username} ya existe")

print(f"\nListo. {len(USUARIOS)} usuarios procesados.")
