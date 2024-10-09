from rest_framework import serializers
from ..models import Estudiante

class EstudianteSerializer(serializers.ModelSerializer):
    
    idmatricula_display = serializers.StringRelatedField(source='idmatricula', read_only=True)
    
    class Meta:
        model = Estudiante
        fields = '__all__'