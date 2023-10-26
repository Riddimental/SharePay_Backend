from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.http import HttpResponse
from .serializer import *
from .models import *


def hello_world(request):
   return HttpResponse("¡Hola, mundo!")

def vistas(request):
   return HttpResponse('sisas')

def defaultViews(request):
   return HttpResponse('bienvenido')

class UsuariosDetailView(APIView):
    def get(self, request):
        # Obten el valor del parámetro 'email' de la consulta
        email = request.query_params.get('email')

        # Realiza la búsqueda en la base de datos
        try:
            usuario = Usuarios.objects.get(CorreoElectronico=email)
        except Usuarios.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Serializa el usuario y devuelve la respuesta
        serializer = UsuariosSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsuariosView(viewsets.ModelViewSet):
   serializer_class = UsuariosSerializer
   queryset = Usuarios.objects.all()
   
class PasswordsView(viewsets.ModelViewSet):
   serializer_class = PasswordsSerializer
   queryset = Passwords.objects.all()
   

class PasswordsDetailView(APIView):
    def get(self, request):
        # Obtén el valor del parámetro 'email' de la consulta
        email = request.query_params.get('email')

        # Realiza la búsqueda en la base de datos
        try:
            password_entry = Passwords.objects.get(CorreoElectronico=email)
        except Passwords.DoesNotExist:
            return Response({"error": "contraseña incorrecta"}, status=status.HTTP_404_NOT_FOUND)

        # Serializa la entrada de contraseña y devuelve la respuesta
        serializer = PasswordsSerializer(password_entry)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
   