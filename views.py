from rest_framework import viewsets, filters
from .models import Instituto
from .serializers import InstitutoSerializer

class InstitutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Puesto Alumno 3: Implementación de ReadOnlyModelViewSet 
    para cumplir con la arquitectura de solo lectura.
    """
    # prefetch_related optimiza la consulta de los ciclos vinculados
    queryset = Instituto.objects.all().prefetch_related('ciclos')
    serializer_class = InstitutoSerializer
    
    # Dejamos preparada la lógica de filtrado para el Alumno 4
    filter_backends = [filters.SearchFilter]
    search_fields = ['ciclos__nombre'] # Permite buscar por el nombre del ciclo [cite: 23]
