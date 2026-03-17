import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario
username = 'admin'
email = 'admin@test.com'
password = 'Admin123456'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✓ Superusuario creado exitosamente")
    print(f"  Usuario: {username}")
    print(f"  Email: {email}")
    print(f"  Contraseña: {password}")
else:
    print(f"✓ Superusuario '{username}' ya existe")

