from rest_framework import serializers
from ..models import Datosmedicos, Eps, Rh

class DatosMedicosSerializer(serializers.ModelSerializer):
    # Para mostrar los nombres de las relaciones
    ideps_display = serializers.StringRelatedField(source='ideps', read_only=True)
    idrh_display = serializers.StringRelatedField(source='idrh', read_only=True)
    
    # Para aceptar IDs en solicitudes POST y PUT
    ideps = serializers.PrimaryKeyRelatedField(queryset=Eps.objects.all())
    idrh = serializers.PrimaryKeyRelatedField(queryset=Rh.objects.all())
    
    class Meta: 
        model = Datosmedicos
        fields = ['iddatosmedicos', 'lugaratencion', 'peso', 'altura', 'idusuario', 
                  'ideps', 'idrh', 'ideps_display', 'idrh_display']