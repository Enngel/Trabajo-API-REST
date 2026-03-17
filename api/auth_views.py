"""
Vistas de autenticación: Login, Registro y Logout
"""

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import re


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Vista de inicio de sesión.
    GET: Muestra formulario de login
    POST: Procesa credenciales (form o JSON)
    """
    if request.method == "POST":
        # Soportar JSON además de form-encoded
        if request.content_type == 'application/json':
            try:
                payload = json.loads(request.body.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                return JsonResponse({'detail': 'JSON inválido'}, status=400)
            email = payload.get('email', '').strip()
            password = payload.get('password', '')
        else:
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

        # Validar que no estén vacíos
        if not email or not password:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Email y contraseña son requeridos'}, status=400)
            messages.error(request, ' Email y contraseña son requeridos')
            return render(request, 'login.html')

        # Buscar usuario por email
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Email o contraseña incorrectos'}, status=401)
            messages.error(request, ' Email o contraseña incorrectos')
            return render(request, 'login.html')

        # Autenticar con username y password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Autenticado', 'username': user.username, 'email': user.email}, status=200)
            messages.success(request, f' Bienvenido {user.first_name}!')
            return redirect('dashboard')
        else:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Email o contraseña incorrectos'}, status=401)
            messages.error(request, ' Email o contraseña incorrectos')
            return render(request, 'login.html')

    # GET: Mostrar formulario
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'login.html')


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    Vista de registro de nuevos usuarios.
    GET: Muestra formulario de registro
    POST: Crea nuevo usuario (form o JSON)
    """
    if request.method == "POST":
        # Soportar JSON además de form-encoded
        if request.content_type == 'application/json':
            try:
                payload = json.loads(request.body.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                return JsonResponse({'detail': 'JSON inválido'}, status=400)
            first_name = payload.get('first_name', '').strip()
            last_name = payload.get('last_name', '').strip()
            email = payload.get('email', '').strip()
            username = payload.get('username', '').strip()
            password = payload.get('password', '')
            password_confirm = payload.get('password_confirm', '')
        else:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '')
            password_confirm = request.POST.get('password_confirm', '')

        # 1. Campos requeridos
        if not all([first_name, last_name, email, username, password, password_confirm]):
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Todos los campos son requeridos'}, status=400)
            messages.error(request, ' Todos los campos son requeridos')
            return render(request, 'register.html')

        # 2. Validar email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Email inválido'}, status=400)
            messages.error(request, ' Email inválido')
            return render(request, 'register.html')

        # 3. Validar contraseña no vacía
        if len(password) < 8:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'La contraseña debe tener al menos 8 caracteres'}, status=400)
            messages.error(request, ' La contraseña debe tener al menos 8 caracteres')
            return render(request, 'register.html')

        # 4. Validar contraseñas coinciden
        if password != password_confirm:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Las contraseñas no coinciden'}, status=400)
            messages.error(request, ' Las contraseñas no coinciden')
            return render(request, 'register.html')

        # 5. Validar que tenga números y letras
        if not re.search(r'[0-9]', password) or not re.search(r'[a-zA-Z]', password):
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'La contraseña debe contener números y letras'}, status=400)
            messages.error(request, ' La contraseña debe contener números y letras')
            return render(request, 'register.html')

        # 6. Validar que no sea todo números
        if password.isdigit():
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'La contraseña no puede ser solo números'}, status=400)
            messages.error(request, ' La contraseña no puede ser solo números')
            return render(request, 'register.html')

        # 7. Verificar que email no exista
        if User.objects.filter(email=email).exists():
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Este email ya está registrado'}, status=400)
            messages.error(request, ' Este email ya está registrado')
            return render(request, 'register.html')

        # 8. Verificar que username no exista
        if User.objects.filter(username=username).exists():
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Este nombre de usuario ya está en uso'}, status=400)
            messages.error(request, ' Este nombre de usuario ya está en uso')
            return render(request, 'register.html')

        # CREAR USUARIO
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Autologin después del registro
            login(request, user)
            if request.content_type == 'application/json':
                return JsonResponse({'detail': 'Cuenta creada', 'username': user.username, 'email': user.email}, status=201)
            messages.success(request, f' ¡Cuenta creada exitosamente! Bienvenido {first_name}')
            return redirect('dashboard')

        except IntegrityError as e:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': f'Error al crear la cuenta: {str(e)}'}, status=500)
            messages.error(request, f' Error al crear la cuenta: {str(e)}')
            return render(request, 'register.html')
        except Exception as e:
            if request.content_type == 'application/json':
                return JsonResponse({'detail': f'Error inesperado: {str(e)}'}, status=500)
            messages.error(request, f' Error inesperado: {str(e)}')
            return render(request, 'register.html')

    # GET: Mostrar formulario
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'register.html')


@login_required(login_url='login')
@require_http_methods(["POST"])
def logout_view(request):
    """
    Vista para cerrar sesión.
    POST: Cierra la sesión y redirige al login
    """
    logout(request)
    messages.success(request, ' Sesión cerrada correctamente')
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    """
    Dashboard del usuario autenticado.
    Muestra opciones de búsqueda y perfil.
    """
    context = {
        'user': request.user,
    }
    return render(request, 'dashboard.html', context)


def home_view(request):
    """
    Página de inicio del sitio.
    Muestra información general y opciones de acceso.
    """
    return render(request, 'home.html')
