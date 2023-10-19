from rest_framework import serializers
from .models import Usuarios

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        #fields = ('id', 'title', 'description', 'done')
        fields = '__all__'