from rest_framework import serializers
from ..models import Usuario, Estudiante, Profesor, Admin
from ..helpers import validateCantDocumento, validateMinCaractEspecial

class UsuarioSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'contrasena': {'write_only': True}} #LA CONTRASEÑA NO SEA ENVIADA
            
    #Funcion que evitará que se cree un usuario con el mismo numero de documento
    def validarDocumento(self, value):
        user = Usuario.objects.filter(documento = value).count()
        #Si encuentra usuarios con ese numero de documento, retornará la cantidad de estos, lo que significa que ese usuario ya existe
        if user >= 1 :
            return False
        
        return True
    
    def validate_nombre(self, value):

        regex = validateMinCaractEspecial(value, "nombre")
        if not regex['result']:
            raise serializers.ValidationError(regex['error'])
        return value 

    def validate_documento(self, value):

        tipoDoc = str(self.initial_data.get('idtipodocumento'))
        validacion = validateCantDocumento(value, tipoDoc)
        
        if not validacion['result']:
            raise serializers.ValidationError([validacion['error']])
            
        return value
    
    
    def create(self, validated_data):
        #Validacion del numero de documento
        numDocumento = validated_data.get('documento')
        validacion = self.validarDocumento(numDocumento)
        if not validacion :
            raise serializers.ValidationError(
                {
                "message" : "Creacion cancelada", 
                "error" : {
                    "documento" : ["Documento ya existe"]
                    }
                 }
                )
        
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['contrasena'])
        usuario.save()
        
        return usuario

    def update(self, instance, validated_data):
        
        if 'contrasena' in validated_data:
            instance.set_password(validated_data['contrasena'])
            validated_data.pop('contrasena', None)
            
        return super().update(instance, validated_data)
