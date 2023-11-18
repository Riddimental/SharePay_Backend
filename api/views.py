from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Q
from django.views import View
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *


def defaultViews(request):
   return HttpResponse('backend de Sharepay')

def have_common_events(request):
    profile1 = request.GET.get('Emisor')
    profile2 = request.GET.get('Remitente')
    events_profile1 = ParticipantesEvento.objects.filter(Apodo=profile1, Estado='activo').values_list('EventoID', flat=True)
    events_profile2 = ParticipantesEvento.objects.filter(Apodo=profile2, Estado='activo').values_list('EventoID', flat=True)

    # Check for common events
    common_events = list(set(events_profile1).intersection(events_profile2))

    return JsonResponse({'common_events': common_events})



def get_user_contacts(request):
    # Obtén el nombre de usuario desde la solicitud GET
    username = request.GET.get('username')

    # Obtiene el objeto User asociado al nombre de usuario proporcionado
    user = get_object_or_404(User, username=username)

    # Obtiene todos los contactos del usuario
    user_contacts = Contactos.objects.all()

    # Serializa los datos si es necesario y devuelve una respuesta JSON
    data = [{
       'emisor': {
            'username': contacto.Emisor.user.username,
            'avatar': contacto.Emisor.FotoOAvatar,
        },
        'remitente': {
            'username': contacto.Remitente.user.username,
            'avatar': contacto.Remitente.FotoOAvatar,
        },
        'estado': contacto.Estado
    } for contacto in user_contacts]
    return JsonResponse({'user_contacts': data})

def get_user(request):
    username = request.GET.get('username')
    email = request.GET.get('email')

    # Verifica si se proporciona un nombre de usuario o un correo electrónico
    if username:
        user = get_object_or_404(User, username=username)
    elif email:
        user = get_object_or_404(User, email=email)
    else:
        # Si no se proporciona ni nombre de usuario ni correo electrónico, devuelve una respuesta de error
        return JsonResponse({'error': 'Debes proporcionar un nombre de usuario o un correo electrónico'}, status=400)

    user_data = {
        'user_id': user.id,
        'username': user.username,
        'password': user.password,  # Ten en cuenta que devolver la contraseña no es seguro en un entorno de producción
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

class CreateContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usuario_emisor = request.data.get('Emisor')
        usuario_remitente = request.data.get('Remitente')

        # Verificar si el contacto ya existe
        existing_contact = Contactos.objects.filter(Q(Emisor=usuario_emisor, Remitente=usuario_remitente)).first()

        # Verifica si está solicitando a una persona que ya había solicitado al propietario
        incoming_invitation = Contactos.objects.filter(Q(Emisor=usuario_remitente, Remitente=usuario_emisor)).first()

        if existing_contact:
            return Response({'message': 'El contacto ya existe'}, status=status.HTTP_400_BAD_REQUEST)

        if incoming_invitation:
            # Verificar que la solicitud esté pendiente antes de actualizar
            if incoming_invitation.Estado == 'Pendiente':
                # Actualizar el estado del contacto a 'Aceptada'
                incoming_invitation.Estado = 'Aceptada'
                incoming_invitation.save()

                return Response({'message': 'Este usuario ya te había invitado, contacto agregado exitosamente'})
             
            # Si la solicitud ya estaba aceptada
            if incoming_invitation.Estado == 'Aceptada':
                return Response({'message': 'Este usuario ya fue creado anteriormente'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear un nuevo contacto
        emisor_instance = get_object_or_404(Perfil, user=usuario_emisor)
        remitente_instance = get_object_or_404(Perfil, user=usuario_remitente)

        nuevo_contacto = Contactos.objects.create(Emisor=emisor_instance, Remitente=remitente_instance, Estado='Pendiente')

        return Response({'message': 'Contacto creado exitosamente'})


class UpdateContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usuario_emisor = request.data.get('Emisor')
        usuario_remitente = request.data.get('Remitente')
        estado_to_update = request.data.get('Estado')
        
        # Use Q objects to combine multiple conditions
        Contacto = get_object_or_404(
            Contactos, Q(Emisor=usuario_emisor) & Q(Remitente=usuario_remitente)
        )
        
        # Get the user instance for the Emisor
        emisor_instance = get_object_or_404(Perfil, user=usuario_emisor)

        # Obtener datos del Contacto desde la solicitud
        remitente_instance = get_object_or_404(Perfil, user=usuario_remitente)

        # Actualizar los campos del Contacto
        Contacto.Emisor = emisor_instance or Contacto.Emisor
        Contacto.Remitente = remitente_instance or Contacto.Remitente
        Contacto.Estado = estado_to_update or Contacto.Estado

        # Guardar los cambios en la base de datos
        Contacto.save()

        return Response({'message': 'Contactos actualizados exitosamente'})
    
    
class DeleteContactsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usuario_emisor = request.data.get('Emisor')
        usuario_remitente = request.data.get('Remitente')
        
        # Verificar si el usuario actual es el propietario del contacto
        contacto = get_object_or_404(
            Contactos,
            (Q(Emisor=usuario_emisor, Remitente=usuario_remitente) | Q(Emisor=usuario_remitente, Remitente=usuario_emisor))
        )

        # Eliminar el contacto de la base de datos
        contacto.delete()

        return Response({'message': 'Contacto eliminado exitosamente'})

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
   filter_backends = [SearchFilter]
   search_fields = ['user__username']
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
   