from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *


def defaultViews(request):
   return HttpResponse('backend de Sharepay')

def get_user_by_username(request):
   username = request.GET.get('username')
   user = get_object_or_404(User, username=username)
   user_data = {
      'user_id': user.id,
      'username': user.username,
      'password': user.password,
      'email': user.email,
      'first_name': user.first_name,
      'last_name': user.last_name,
      'is_active': user.is_active,
   }
   return JsonResponse(user_data)



class UpdateUserView(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request, *args, **kwargs):
      # Obtener datos del usuario desde la solicitud
      usuario = request.data.get('username')
      email = request.data.get('email')
      first_name = request.data.get('first_name')
      last_name = request.data.get('last_name')
      password = request.data.get('password')
      is_active = request.data.get('is_active', True)  # Valor predeterminado es True si no se proporciona


      # Buscar el usuario existente por nombre de usuario
      user = get_object_or_404(User, username=usuario)

      # Actualizar los campos del usuario
      user.email = email or user.email
      user.first_name = first_name or user.first_name
      user.last_name = last_name or user.last_name
      user.is_active = is_active
      if password:
          # Validar y requerir contraseñas seguras si es necesario
          user.set_password(password)
      user.save()

      return Response({'message': 'Usuario actualizado exitosamente'})

class UpdateProfileView(APIView):
   permission_classes = [IsAuthenticated]
   
   def post(self, request, *args, **kwargs):
      usuario = request.data.get('username')
      user = get_object_or_404(Perfil, user=usuario)

      # Obtener datos del perfil desde la solicitud
      foto_avatar = request.data.get('FotoOAvatar', user.FotoOAvatar)
      bio = request.data.get('bio', user.bio)

      # Actualizar los campos del perfil
      user.FotoOAvatar = foto_avatar or user.FotoOAvatar
      user.bio = bio or user.bio

      # Guardar los cambios en la base de datos
      user.save()

      return Response({'message': 'Perfil actualizado exitosamente'})




class LogInView(ObtainAuthToken):
   permission_classes = [AllowAny]
   authentication_classes = []
   def post(self, request, *args, **kwargs):
        # Personaliza el uso de 'username' en lugar de 'email'
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class LogOutView(APIView):
   def get(self, request, format=None):
      request.user.auth_token.delete()
      return Response(status=status.HTTP_200_OK)


class SignUpView(CreateAPIView):
   permission_classes = [AllowAny]
   authentication_classes = []
   queryset = User.objects.all()
   serializer_class = SignUpSerializer


class PerfilView(viewsets.ModelViewSet):
   permission_classes = [IsAuthenticated]
   serializer_class = PerfilSerializer
   queryset = Perfil.objects.all()
   http_method_names = ['get', 'post']

   


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
   