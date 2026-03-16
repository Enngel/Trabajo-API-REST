from rest_framework import viewsets, filters
from .models import Instituto
from .serializers import InstitutoSerializer

class InstitutoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Instituto.objects.all()
    serializer_class = InstitutoSerializer

    # Filtros obligatorios según el diseño del proyecto
    filter_backends = [filters.SearchFilter]
    search_fields = ['ciclos__nombre']  # Permite ?search=DAW

    # Si queréis usar ?ciclo= en vez de ?search=
    def get_queryset(self):
        qs = super().get_queryset()
        ciclo = self.request.query_params.get('ciclo')

        if ciclo:
            qs = qs.filter(ciclos__nombre__icontains=ciclo)

        return qs