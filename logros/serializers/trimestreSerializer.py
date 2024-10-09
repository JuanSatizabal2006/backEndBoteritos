from rest_framework import serializers
from ..models import Trimestres

class TrimestreSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Trimestres
        fields = '__all__'
        