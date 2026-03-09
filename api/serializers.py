from rest_framework import serializers
from .models import Instituto, CicloFormativo

class CicloFormativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloFormativo
        fields = '__all__'

class InstitutoSerializer(serializers.ModelSerializer):
    # This will include the related 'ciclos' in the output
    ciclos = CicloFormativoSerializer(many=True, read_only=True)

    class Meta:
        model = Instituto
        fields = '__all__'