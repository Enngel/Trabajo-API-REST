from rest_framework import generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Instituto, CicloFormativo
from .serializers import (
    InstitutoSerializer,
    CicloFormativoSerializer,
    CicloFormativoSearchSerializer
)


class InstitutoListView(generics.ListAPIView):
    """
    Lista todos los institutos con opciones avanzadas de búsqueda y filtrado.

    Parámetros de query:
    - search: buscar por nombre o municipio (búsqueda de texto libre)
    - keywords: buscar por palabras clave exactas separadas por comas
    - municipio: filtrar por municipio exacto
    - titularidad: filtrar por titularidad (Público/Privado)
    - tipo: filtrar por tipo de centro (IES, CIFP, etc.)
    - lat,lon: latitud y longitud para filtrar por distancia
    - distance: distancia en km (default: 50)
    - ordering: ordenar por 'nombre', 'municipio' o '-municipio'

    Ejemplos:
    - GET /api/institutos/?search=pio
    - GET /api/institutos/?keywords=informática,programación
    - GET /api/institutos/?municipio=Madrid&tipo=IES
    - GET /api/institutos/?lat=40.4168&lon=-3.7038&distance=20
    """
    queryset = Instituto.objects.all().prefetch_related('ciclos')
    serializer_class = InstitutoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda de texto libre (case-insensitive)
    search_fields = ['nombre', 'municipio', 'direccion', 'tipo', 'titularidad', 'keywords']

    # Filtrado exacto
    filterset_fields = ['municipio', 'titularidad', 'tipo', 'situacion']

    # Ordenamiento
    ordering_fields = ['nombre', 'municipio', 'tipo', 'titularidad']
    ordering = ['municipio', 'nombre']

    def get_queryset(self):
        """Filtra por distancia si se proporcionan coordenadas"""
        queryset = super().get_queryset()

        # Filtrar por palabras clave (keywords)
        keywords = self.request.query_params.get('keywords')
        if keywords:
            keyword_list = [k.strip().lower() for k in keywords.split(',')]
            keyword_query = Q()
            for keyword in keyword_list:
                keyword_query |= Q(keywords__icontains=keyword) | Q(nombre__icontains=keyword)
            queryset = queryset.filter(keyword_query)

        # Filtrar por distancia (geolocalización)
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                distance_km = float(self.request.query_params.get('distance', 50))

                # Filtrar institutos dentro del radio de distancia
                filtered_institutos = []
                for instituto in queryset:
                    dist = instituto.get_distance_to(lat, lon)
                    if dist <= distance_km:
                        filtered_institutos.append(instituto.codigo)

                queryset = queryset.filter(codigo__in=filtered_institutos)
            except (ValueError, TypeError):
                pass

        return queryset


class InstitutoDetailView(generics.RetrieveAPIView):
    """
    Detalle de un instituto específico por su código (pk).
    Incluye todos los ciclos formativos que imparte.

    Parámetros de query:
    - lat,lon: coordenadas para calcular distancia
    """
    queryset = Instituto.objects.all().prefetch_related('ciclos')
    serializer_class = InstitutoSerializer


class CicloFormativoSearchView(generics.ListAPIView):
    """
    Búsqueda avanzada de ciclos formativos.

    Soporta búsqueda por:
    - Nombre completo (búsqueda de texto libre)
    - Abreviación/Código (ej: DAW, ASIR, CF)
    - Familia profesional

    Parámetros de query:
    - search: búsqueda de texto libre en nombre, descripción, abreviación
    - abreviacion: búsqueda exacta o parcial de código (ej: DAW)
    - familia: filtrar por familia profesional
    - grado: filtrar por grado (Medio/Superior)

    Ejemplos:
    - GET /api/ciclos/?search=desarrollo
    - GET /api/ciclos/?abreviacion=DAW
    - GET /api/ciclos/?familia=Informática
    - GET /api/ciclos/?search=web
    """
    queryset = CicloFormativo.objects.prefetch_related('institutos')
    serializer_class = CicloFormativoSearchSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Búsqueda de texto libre
    search_fields = ['nombre', 'abreviacion', 'familia_profesional', 'descripcion']

    # Filtrado exacto
    filterset_fields = ['familia_profesional', 'grado']

    # Ordenamiento
    ordering_fields = ['nombre', 'familia_profesional']
    ordering = ['nombre']

    def get_queryset(self):
        """Filtrar por abreviación si se proporciona"""
        queryset = super().get_queryset()

        abreviacion = self.request.query_params.get('abreviacion')
        if abreviacion:
            # Búsqueda insensible a mayúsculas/minúsculas
            queryset = queryset.filter(abreviacion__iexact=abreviacion)

        return queryset


class CicloFormativoDetailView(generics.RetrieveAPIView):
    """
    Detalle de un ciclo formativo específico.
    Incluye todos los institutos que lo imparten.
    """
    queryset = CicloFormativo.objects.prefetch_related('institutos')
    serializer_class = CicloFormativoSearchSerializer
    lookup_field = 'id'


class CicloFormativoByInstitutoView(generics.ListAPIView):
    """
    Lista ciclos de un instituto específico.

    GET /api/institutos/{codigo}/ciclos/
    """
    serializer_class = CicloFormativoSerializer

    def get_queryset(self):
        """Obtiene ciclos del instituto especificado"""
        codigo = self.kwargs.get('codigo')
        try:
            instituto = Instituto.objects.get(codigo=codigo)
            return instituto.ciclos.all()
        except Instituto.DoesNotExist:
            return CicloFormativo.objects.none()


