from rest_framework import serializers
from ..models import Historiaclinica, Condicion, Diagnostico, Discapacidad

class HistoriaClinicaSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Historiaclinica
        fields = '__all__'

class CondicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condicion
        fields = '__all__'

class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = '__all__'
        
class DiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discapacidad
        fields = '__all__'