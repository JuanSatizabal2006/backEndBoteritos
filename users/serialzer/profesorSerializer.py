from rest_framework import serializers
from ..models import Profesor,Areas

class ProfesorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profesor
        fields = '__all__'