from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from .models import *


def defaultViews(request):
   return HttpResponse('backend de Sharepay')

@method_decorator(csrf_exempt, name='dispatch')
class UpdateUserView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.post('username')
        user = get_object_or_404(User, username=username)

        user.email = request.POST.post('email', user.email)
        user.first_name = request.POST.post('first_name', user.first_name)
        user.last_name = request.POST.post('last_name', user.last_name)
        user.password = request.POST.post('password', user.password)

        # Guarda los cambios en la base de datos
        user.save()

        user_data = {
            'username': user.username,
        }

        return JsonResponse(user_data)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.post('username')
        user = get_object_or_404(Perfil, username=username)

        user.FotoOAvatar = request.POST.post('FotoOAvatar', user.FotoOAvatar)
        user.bio = request.POST.post('bio', user.bio)

        # Guarda los cambios en la base de datos
        user.save()

        user_data = {
            'username': user.username
        }

        return JsonResponse(user_data)


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
    }
    return JsonResponse(user_data)

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

   def list(self, request, *args, **kwargs):
      queryset = self.filter_queryset(self.get_queryset())
      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)

   def create(self, request, *args, **kwargs):
      # Lógica para crear un nuevo perfil a partir de los datos del request
      serializer = PerfilSerializer(data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def retrieve(self, request, *args, **kwargs):
      instance = self.get_object()
      serializer = self.get_serializer(instance)
      return Response(serializer.data)

   def retrieve_by_username(self, request, *args, **kwargs):
      # Modificar la función para buscar por username
      username = kwargs.get('username')
      instance = self.get_object_by_username(username)
      serializer = self.get_serializer(instance)
      return Response(serializer.data)

   def get_object_by_username(self, username):
      # Modificar la función para buscar por username
      try:
         return Perfil.objects.get(usuario__username=username)
      except Perfil.DoesNotExist:
         raise Http404("Perfil no encontrado")


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
   