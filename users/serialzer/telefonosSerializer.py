from rest_framework import serializers
from ..models import Telefonos

class TelefonosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefonos
        fields = '__all__'