from django.contrib import admin
from django.urls import path, include  # <-- IMPORTANTE: añade 'include' aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # <-- AÑADE ESTA LÍNEA
]