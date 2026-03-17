from django.contrib import admin
from .models import Instituto, CicloFormativo


@admin.register(CicloFormativo)
class CicloFormativoAdmin(admin.ModelAdmin):
    """Admin para ciclos formativos"""
    list_display = ('nombre', 'familia_profesional', 'grado')
    search_fields = ('nombre', 'familia_profesional')
    list_filter = ('grado', 'familia_profesional')
    ordering = ('familia_profesional', 'nombre')


@admin.register(Instituto)
class InstitutoAdmin(admin.ModelAdmin):
    """Admin para institutos educativos"""

    # Columnas en la vista de lista
    list_display = ('codigo', 'nombre', 'municipio', 'tipo', 'titularidad', 'situacion')

    # Búsqueda rápida
    search_fields = ('codigo', 'nombre', 'municipio', 'direccion', 'email')

    # Filtros laterales
    list_filter = ('tipo', 'titularidad', 'situacion', 'municipio')
    
    # Paginación
    list_per_page = 50

    # Interfaz para seleccionar ciclos (más cómoda que input de texto)
    filter_horizontal = ('ciclos',)
    
    # Agrupación de campos en la edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'tipo', 'titularidad', 'situacion'),
            'description': 'Datos principales del centro educativo'
        }),
        ('Ubicación', {
            'fields': ('municipio', 'direccion', 'codigo_postal', 'latitud', 'longitud'),
            'description': 'Localización geográfica'
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'web'),
            'description': 'Datos de contacto'
        }),
        ('Oferta Educativa', {
            'fields': ('ciclos',),
            'description': 'Ciclos formativos que imparte'
        }),
    )

    # Campo de solo lectura
    readonly_fields = ('codigo',)

