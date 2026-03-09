from django.contrib import admin
from .models import Instituto, CicloFormativo

@admin.register(CicloFormativo)
class CicloFormativoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'familia_profesional', 'grado')
    search_fields = ('nombre', 'familia_profesional')
    list_filter = ('grado',)

@admin.register(Instituto)
class InstitutoAdmin(admin.ModelAdmin):
    # Columnas que se ven en el listado
    list_display = ('codigo', 'nombre', 'municipio', 'tipo', 'situacion')
    
    # Buscador (muy útil para el Alumno 1 y 3)
    search_fields = ('codigo', 'nombre', 'municipio', 'direccion')
    
    # Filtros laterales
    list_filter = ('tipo', 'titularidad', 'situacion', 'municipio')
    
    # Interfaz para seleccionar ciclos (Mucho más cómoda)
    filter_horizontal = ('ciclos',)
    
    # Agrupación de campos en la edición
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'tipo', 'titularidad', 'situacion')
        }),
        ('Ubicación', {
            'fields': ('municipio', 'direccion', 'codigo_postal', 'latitud', 'longitud')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email', 'web')
        }),
        ('Oferta Educativa', {
            'fields': ('ciclos',)
        }),
    )