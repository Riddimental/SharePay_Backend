from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
   email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

   password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
   password2 = serializers.CharField(write_only=True, required=True)
   first_name = serializers.CharField(write_only=True, required=True)
   last_name = serializers.CharField(write_only=True, required=True)

   class Meta:
      model = User
      fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

   def validate(self, attrs):
      if attrs['password'] != attrs['password2']:
         raise serializers.ValidationError({"password": "Password fields didn't match."})

      return attrs

   def create(self, validated_data):
      user = User.objects.create(
         username=validated_data['username'],
         email=validated_data['email'],
         first_name=validated_data['first_name'],
         last_name=validated_data['last_name']
      )
      
      user.set_password(validated_data['password'])
      user.save()

      return user


class PerfilSerializer(serializers.ModelSerializer):
   class Meta:
      model = Perfil
      fields = '__all__'
      
class ContactosSerializer(serializers.ModelSerializer):
   class Meta:
      model = Contactos
      fields = '__all__'
      
class EventosSerializer(serializers.ModelSerializer):
   class Meta:
      model = Eventos
      fields = '__all__'

class ParticipantesEventoSerializer(serializers.ModelSerializer):
   class Meta:
      model = ParticipantesEvento
      fields = '__all__'
      
class ActividadesSerializer(serializers.ModelSerializer):
   class Meta:
      model = Actividades
      fields = '__all__'
      
class ParticipantesActividadSerializer(serializers.ModelSerializer):
   class Meta:
      model = ParticipantesActividad
      fields = '__all__'
      
class SaldosSerializer(serializers.ModelSerializer):
   class Meta:
      model = Saldos
      fields = '__all__'
      
class PagosSerializer(serializers.ModelSerializer):
   class Meta:
      model = Pagos
      fields = '__all__'