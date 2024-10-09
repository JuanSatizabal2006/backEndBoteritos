from rest_framework import serializers
from .models import Tipodocumento, Eps, Rh, Sexo, Areas,Rol,Diagnostico,Discapacidad,Matriculas,Tipologro, Tipoparentesco

class TiposDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipodocumento
        fields = '__all__'

class EpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eps
        fields = '__all__'

class RhSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Rh
        fields = '__all__'

class SexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sexo
        fields = '__all__'
    
class AreasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Areas
        fields = '__all__'
        
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'
        
class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = '__all__'

class DiscapacidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discapacidad
        fields = '__all__'

class MatriculasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matriculas
        fields = '__all__'

class TipologroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipologro
        fields = '__all__'

class TipoparentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoparentesco
        fields = '__all__'