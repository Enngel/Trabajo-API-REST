from rest_framework import serializers
from .models import Instituto, CicloFormativo

class CicloFormativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloFormativo
        # Campos exactos definidos en la estructura de la BBDD del PDF
        fields = ['id', 'nombre', 'familia_profesional', 'grado'] [cite: 30, 31]

class InstitutoSerializer(serializers.ModelSerializer):
    # Relación Many-to-Many anidada para mostrar los ciclos dentro del instituto
    ciclos = CicloFormativoSerializer(many=True, read_only=True) [cite: 23, 32]

    class Meta:
        model = Instituto
        # Incluimos los campos requeridos, incluyendo coordenadas GPS
        fields = ['codigo', 'nombre', 'direccion', 'distrito', 'latitud', 'longitud', 'ciclos'] [cite: 23, 29]
