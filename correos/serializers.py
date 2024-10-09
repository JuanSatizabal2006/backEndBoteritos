from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = '__all__'
    
    def update(self, instance, validated_data):
        
        if 'contrasena' in validated_data:
            instance.set_password(validated_data['contrasena'])
            validated_data.pop('contrasena', None)
            
        return super().update(instance, validated_data)