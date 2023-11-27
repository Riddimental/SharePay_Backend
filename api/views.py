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
            'id' : contacto.Emisor.user.id,
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

def get_user_events(request):
    # Obtén el nombre de usuario desde la solicitud GET
    username = request.GET.get('username')
    
    # obtiene los eventos en los que el usuario esta participando
    participations = ParticipantesEvento.objects.filter(Apodo=username)
    

    # Obtiene todos los eventos del usuario
    events = Eventos.objects.all()

    # Serializa los datos y devuelve una respuesta JSON
    data = [{
        'Apodo': participant.Apodo,
        'EventoID': participant.Nom
    } for participant in participations]
    return JsonResponse({'user_events': data})

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
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_active': user.is_active,
    }

    return JsonResponse(user_data)

def get_participants(request):
    username = request.GET.get('username')

    participants = ParticipantesEvento.objects.filter(Apodo__user__username=username)

    if not participants.exists():
        return JsonResponse({'error': 'No se encontraron participantes con ese apodo'}, status=404)

    participants_data = [
        {
            'Apodo': participant.Apodo.user.username,
            'Evento': {
                'EventoID': participant.EventoID.EventoID,
                'Nombre': participant.EventoID.Nombre,
                'Descripcion': participant.EventoID.Descripcion,
                'Avatar': participant.EventoID.FotoOAvatar,
                'Tipo': participant.EventoID.Tipo,
                'Creador' : participant.EventoID.Creador.user.username,
            },
            'Estado': participant.Estado
        }
        for participant in participants
    ]

    return JsonResponse({'participants': participants_data}, safe=False)

def get_event_activities(request):
    #obtengo el nombre del evento del request
    evento_ID = request.GET.get('eventID')
    #obtengo las actividades relacionadas al evento que tenga el mismo nombre que el proporcionado
    actividades_evento = Actividades.objects.filter(EventoID_id=evento_ID)
    
    if not actividades_evento.exists():
        return JsonResponse({'alerta': 'No se encontraron actividades para ese evento'})
    
    activities_data = [
        {
            'Creador': activity.Creador.user.username,
            'Nombre': activity.Nombre,
            'Descripcion': activity.Descripcion,
            'Valor': str(activity.ValorTotal),
        }
        for activity in actividades_evento
    ]
    
    return JsonResponse({'activities': activities_data}, safe=False)
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
        existing_contact = Contactos.objects.filter(
            (Q(Emisor=usuario_emisor, Remitente=usuario_remitente))
        ).first()

        if existing_contact:
            return Response({'message': 'El contacto ya existe'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Verificar si el contacto inverso ya existe
        reverse_contact_exists = Contactos.objects.filter(
            Q(Emisor=usuario_remitente, Remitente=usuario_emisor)
        ).exists()

        if reverse_contact_exists:
            return Response({'message': 'El contacto inverso ya existe'}, status=status.HTTP_400_BAD_REQUEST)



        # Crear un nuevo contacto
        emisor_instance = get_object_or_404(Perfil, user=usuario_emisor)
        remitente_instance = get_object_or_404(Perfil, user=usuario_remitente)

        nuevo_contacto = Contactos.objects.create(Emisor=emisor_instance, Remitente=remitente_instance, Estado='Pendiente')

        return Response({'message': 'Contacto creado exitosamente'})


class CreateEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Obtén los datos de la solicitud
        creador = request.data.get('creador')
        evento_creador = get_object_or_404(Perfil, user=creador)
        evento_nombre = request.data.get('evento')
        evento_descripcion = request.data.get('descripcion', '')  # Podría ser opcional
        evento_tipo = request.data.get('tipo', '')  # Podría ser opcional
        evento_foto = request.data.get('avatar', '')  # Podría ser opcional

        # Verifica si el evento ya existe para el creador dado
        existing_event = Eventos.objects.filter(Q(Creador=evento_creador, Nombre=evento_nombre)).first()

        if existing_event:
            return Response({'error': 'El evento ya existe para este creador'}, status=status.HTTP_400_BAD_REQUEST)

        # Crea el nuevo evento
        nuevo_evento = Eventos.objects.create(
            Creador=evento_creador,
            Nombre=evento_nombre,
            Descripcion=evento_descripcion,
            Tipo=evento_tipo,
            FotoOAvatar=evento_foto
        )

        return Response({'message': 'Evento creado exitosamente'}, status=status.HTTP_201_CREATED)

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
    

class UpdateEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        evento_id = request.data.get('id')
        evento_nombre = request.data.get('nombre')
        evento_descripcion = request.data.get('descripcion')
        evento_tipo = request.data.get('tipo')
        
        # Use Q objects to combine multiple conditions
        Evento = get_object_or_404(
            Eventos, Q(EventoID=evento_id)
        )

        # Actualizar los campos del Contacto
        Evento.Nombre = evento_nombre or Evento.Nombre
        Evento.Descripcion = evento_descripcion or Evento.Descripcion
        Evento.Tipo = evento_tipo or Evento.Tipo

        # Guardar los cambios en la base de datos
        Evento.save()

        return Response({'message': 'Evento actualizado exitosamente'})
    
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
    
class DeleteEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        evento_id = request.data.get('eventID')
        
        # Verificar si el usuario actual es el propietario del contacto
        evento = get_object_or_404(Eventos,(Q(EventoID=evento_id)))

        # Eliminar el contacto de la base de datos
        evento.delete()

        return Response({'message': 'Evento eliminado exitosamente'})

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
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipantesEventoSerializer
    queryset = ParticipantesEvento.objects.all()  # Ajusta esto según tus necesidades

    def create(self, request, *args, **kwargs):
        participant_apodo = request.data.get('Apodo')
        participant_eventoID = request.data.get('EventoID')

        # Verificar si el participante ya existe
        existing_participant = ParticipantesEvento.objects.filter(Q(Apodo=participant_apodo, EventoID=participant_eventoID)).first()

        if existing_participant:
            return Response({'message': 'El usuario ya estaba participando en el evento.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear un nuevo participante
        participante = get_object_or_404(Perfil, user=participant_apodo)
        evento_id = get_object_or_404(Eventos, EventoID=participant_eventoID)

        nuevo_participante = ParticipantesEvento.objects.create(Apodo=participante, EventoID=evento_id)

        serializer = self.get_serializer(nuevo_participante)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   
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
   