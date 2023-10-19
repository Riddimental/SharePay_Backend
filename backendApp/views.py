from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializer import UsuarioSerializer
from .models import Usuarios

def hello_world(request):
   return HttpResponse("¡Hola, mundo!")

def vistas(request):
   return HttpResponse('sisas')

def defaultViews(request):
   return HttpResponse('bienvenido')

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
