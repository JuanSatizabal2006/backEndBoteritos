from rest_framework import serializers
from ..models import Logroestudiante

class CalificarSerializer(serializers.ModelSerializer):
        
    class Meta:
        model =  Logroestudiante
        fields = '__all__'