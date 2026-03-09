from rest_framework import generics, filters
from .models import Instituto
from .serializers import InstitutoSerializer

class InstitutoListView(generics.ListAPIView):
    queryset         = Instituto.objects.all()
    serializer_class = InstitutoSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['nombre', 'municipio']
    ordering_fields  = ['nombre', 'municipio']
    ordering         = ['municipio']

    def get_queryset(self):
        qs          = super().get_queryset()
        municipio   = self.request.query_params.get('municipio')
        titularidad = self.request.query_params.get('titularidad')
        if municipio:
            qs = qs.filter(municipio__icontains=municipio)
        if titularidad:
            qs = qs.filter(titularidad__icontains=titularidad)
        return qs

class InstitutoDetailView(generics.RetrieveAPIView):
    queryset         = Instituto.objects.all()
    serializer_class = InstitutoSerializer
