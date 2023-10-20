from django.http import HttpResponse
from rest_framework import viewsets
from .serializer import *
from .models import *


def hello_world(request):
   return HttpResponse("¡Hola, mundo!")

def vistas(request):
   return HttpResponse('sisas')

def defaultViews(request):
   return HttpResponse('bienvenido')

class UsuariosView(viewsets.ModelViewSet):
   serializer_class = UsuariosSerializer
   queryset = Usuarios.objects.all()
   
class PasswordsView(viewsets.ModelViewSet):
   serializer_class = PasswordsSerializer
   queryset = Passwords.objects.all()
   
class ContactosView(viewsets.ModelViewSet):
   serializer_class = ContactosSerializer
   queryset = Contactos.objects.all()
   
class EventosView(viewsets.ModelViewSet):
   serializer_class = EventosSerializer
   queryset = Eventos.objects.all()
   
class ParticipantesEventoView(viewsets.ModelViewSet):
   serializer_class = ParticipantesEventoSerializer
   queryset = ParticipantesEvento.objects.all()
   
class ActividadesView(viewsets.ModelViewSet):
   serializer_class = ActividadesSerializer
   queryset = Actividades.objects.all()
   
class ParticipantesActividadView(viewsets.ModelViewSet):
   serializer_class = ParticipantesActividadSerializer
   queryset = ParticipantesActividad.objects.all()
   
class SaldosView(viewsets.ModelViewSet):
   serializer_class = SaldosSerializer
   queryset = Saldos.objects.all()
   
class PagosView(viewsets.ModelViewSet):
   serializer_class = PagosSerializer
   queryset = Pagos.objects.all()
   