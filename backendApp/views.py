<<<<<<< HEAD
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializer import UsuarioSerializer
from .models import Usuarios
=======
from django.http import HttpResponse
from rest_framework import viewsets
from .serializer import *
from .models import *

>>>>>>> 94bbe99

def hello_world(request):
   return HttpResponse("¡Hola, mundo!")

def vistas(request):
   return HttpResponse('sisas')

def defaultViews(request):
   return HttpResponse('bienvenido')

<<<<<<< HEAD
@api_view(["POST", "GET"])
def register(request):

   if request.method == 'GET':
      users = Usuarios.objects.all()
      serializer = UsuarioSerializer(users, many=True)
      return Response(serializer.data)

   if request.method == 'POST':
      print(request.data)
      serializer = UsuarioSerializer(data=request.data)
      print(serializer.is_valid())
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
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
   
>>>>>>> 94bbe99
