from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
   return HttpResponse("¡Hola, mundo!")

def vistas(request):
   return HttpResponse('sisas')

def defaultViews(request):
   return HttpResponse('bienvenido')