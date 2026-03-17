from rest_framework import serializers
from .models import Instituto, CicloFormativo


class CicloFormativoSerializer(serializers.ModelSerializer):
    """Serializador para ciclos formativos con todos los campos"""
    class Meta:
        model = CicloFormativo
        fields = ['id', 'nombre', 'abreviacion', 'familia_profesional', 'grado', 'descripcion']


class InstitutoSerializer(serializers.ModelSerializer):
    """Serializador para institutos con ciclos anidados"""
    ciclos = CicloFormativoSerializer(many=True, read_only=True)
    distancia_km = serializers.SerializerMethodField()

    class Meta:
        model = Instituto
        fields = [
            'codigo', 'nombre', 'tipo', 'titularidad', 'municipio', 'distrito',
            'direccion', 'codigo_postal', 'telefono', 'email', 'web',
            'latitud', 'longitud', 'situacion', 'ciclos', 'keywords', 'distancia_km'
        ]

    def get_distancia_km(self, obj):
        """Calcula distancia si se proporcionan coordenadas en context"""
        request = self.context.get('request')
        if request and 'lat' in request.query_params and 'lon' in request.query_params:
            try:
                lat = float(request.query_params.get('lat'))
                lon = float(request.query_params.get('lon'))
                return round(obj.get_distance_to(lat, lon), 2)
            except (ValueError, TypeError):
                return None
        return None


class InstitutoSimpleSerializer(serializers.ModelSerializer):
    """Serializador simple sin ciclos (para búsquedas rápidas)"""
    class Meta:
        model = Instituto
        fields = ['codigo', 'nombre', 'tipo', 'municipio', 'latitud', 'longitud']


class CicloFormativoSearchSerializer(serializers.ModelSerializer):
    """Serializador para búsqueda de ciclos (con institutos)"""
    institutos = InstitutoSimpleSerializer(source='institutos', many=True, read_only=True)

    class Meta:
        model = CicloFormativo
        fields = ['id', 'nombre', 'abreviacion', 'familia_profesional', 'grado', 'institutos']

