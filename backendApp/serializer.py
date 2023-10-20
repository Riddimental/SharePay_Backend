from rest_framework import serializers
from .models import *


class UsuariosSerializer(serializers.ModelSerializer):
   class Meta:
      model = Usuarios
      fields = '__all__'
      
class PasswordsSerializer(serializers.ModelSerializer):
   class Meta:
      model = Passwords
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