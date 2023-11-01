from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *


def hello_world(request):
   return HttpResponse("¡Hola, mundo!")

def vistas(request):
   return HttpResponse('vistas')

def defaultViews(request):
   return HttpResponse('bienvenido')

class LogInView(ObtainAuthToken):
   permission_classes = [AllowAny]
   authentication_classes = []


class LogOutView(APIView):
   def get(self, request, format=None):
      request.user.auth_token.delete()
      return Response(status=status.HTTP_200_OK)


class SignUpView(CreateAPIView):
   permission_classes = [AllowAny]
   authentication_classes = []
   queryset = User.objects.all()
   serializer_class = SignUpSerializer


class UsuariosView(viewsets.ModelViewSet):
   serializer_class = UsuariosSerializer
   queryset = Usuarios.objects.all()
   
   """
   List a queryset.
   """
   def list(self, request, *args, **kwargs):
      print("#"*30)
      print(f"request.user: {request.user}")
      print(f"request.user.id: {request.user.id}")
      print("#"*30)
      queryset = self.filter_queryset(self.get_queryset())

      page = self.paginate_queryset(queryset)
      if page is not None:
         serializer = self.get_serializer(page, many=True)
         return self.get_paginated_response(serializer.data)

      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)

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
   