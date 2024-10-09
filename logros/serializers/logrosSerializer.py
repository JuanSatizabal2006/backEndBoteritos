from rest_framework import serializers
from ..models import Logros, Logroestudiante, Informes

class LogrosSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Logros
        fields = '__all__'
        
class CalificarSerializer(serializers.ModelSerializer):
    # Para mostrar los nombres de las relaciones
    idlogro_display = serializers.StringRelatedField(source='idlogro', read_only=True)
    
    # Para aceptar IDs en solicitudes POST y PUT
    idlogro = serializers.PrimaryKeyRelatedField(queryset=Logros.objects.all())
    
    class Meta:
        model =  Logroestudiante
        fields = '__all__'
        
class InformesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Informes
        fields = '__all__'
    