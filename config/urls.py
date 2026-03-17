from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.auth_views import login_view, register_view, logout_view, dashboard_view, home_view

schema_view = get_schema_view(
    openapi.Info(
        title="API Institutos Madrid",
        default_version='v1',
        description="API de consulta de institutos y ciclos formativos de la Comunidad de Madrid",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # VISTAS WEB (FRONTEND)
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # ADMINISTRADOR
    path('admin/', admin.site.urls),

    # DOCUMENTACIÓN (SWAGGER)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # API REST (DELEGA AL ARCHIVO DE LA APP)
    # Al poner 'api/', Django lo añadirá automáticamente a todo lo que esté en api.urls
    path('api/', include('api.urls')),
]