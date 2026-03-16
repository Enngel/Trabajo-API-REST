from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Institutos y Ciclos Formativos",
        default_version='v1',
        description="API de solo lectura para consultar institutos y ciclos formativos.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de la API
    path('api/', include('api.urls')),

    # Documentación interactiva
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]