from rest_framework import serializers
from ..models import Fechas

class FechasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fechas
        fields = '__all__'