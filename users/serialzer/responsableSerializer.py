from rest_framework import serializers
from ..models import Responsable
from ..helpers import validateCantDocumento, validateMinCaractEspecial

class ResponsableSerializer(serializers.ModelSerializer):

    nombre = serializers.CharField(
        error_messages={
            'required': 'El nombre es obligatorio.',
            'blank' : 'El nombre es obligatorio.'
        }
    )
    
    correo = serializers.EmailField(
        error_messages={
            'required': 'El correo es obligatorio',
            'blank': 'El correo es obligatorio',
            'invalid': 'El formato del correo es inválido'
        }
    )

    numerodocumento = serializers.CharField(
        error_messages={
            'required': 'El número de documento es obligatorio',
            'blank': 'El número de documento es obligatorio',
            'invalid': 'El número de documento debe ser un valor válido'
        }
    )

    telefono = serializers.CharField(
        error_messages={
            'required': 'El teléfono es obligatorio',
            'blank': 'El teléfono es obligatorio',
            'invalid': 'El teléfono debe ser un valor válido'
        }
    )

    profesion = serializers.CharField(
        error_messages={
            'required': 'La profesión es obligatoria',
            'blank': 'La profesión es obligatoria',
            'invalid': 'La profesión debe ser un valor válido'
        }
    )

    ocupacion = serializers.CharField(
        error_messages={
            'required': 'La ocupación es obligatoria',
            'blank': 'La ocupación es obligatoria',
            'invalid': 'La ocupación debe ser un valor válido'
        }
    )

    empresa = serializers.CharField(
        error_messages={
            'required': 'La empresa es obligatoria',
            'blank': 'La empresa es obligatoria',
            'invalid': 'La empresa debe ser un valor válido'
        }
    )

    class Meta:
        model = Responsable
        fields = '__all__'
    
    #Funcion que evitará que se cree un usuario con el mismo numero de documento
    def validarNumeroDocumento(self, value):
        user = Responsable.objects.filter(numerodocumento = value).count()
        #Si encuentra usuarios con ese numero de documento, retornará la cantidad de estos, lo que significa que ese usuario ya existe
        
        if user >= 1 :
            return False
        
        return True
    
    def validate_numerodocumento(self, value):

        tipoDoc = str(self.initial_data.get('idtipodocumento'))
        validacion = validateCantDocumento(value, tipoDoc)
        
        if not validacion['result']:
            raise serializers.ValidationError([validacion['error']])
            
        return value
    
    
    def create(self, validated_data):
        #Validacion del numero de documento
        numDocumento = validated_data.get('numerodocumento')
        validacion = self.validarNumeroDocumento(numDocumento)
        if not validacion :
            raise serializers.ValidationError(
                {
                "message" : "Creacion cancelada", 
                "error" : {
                    "numerodocumento" : ["Documento ya existe"]
                    }
                 }
                )
        
        responsable = Responsable(**validated_data)
        responsable.save()
        
        return responsable
