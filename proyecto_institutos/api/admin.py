from django.contrib import admin
from .models import Instituto

@admin.register(Instituto)
class InstitutoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'municipio', 'distrito', 'titularidad')
    search_fields = ('nombre', 'municipio')
    list_filter   = ('titularidad', 'municipio')
