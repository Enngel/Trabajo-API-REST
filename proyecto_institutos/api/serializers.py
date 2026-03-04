from rest_framework import serializers
from .models import Instituto

class InstitutoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Instituto
        fields = '__all__'
