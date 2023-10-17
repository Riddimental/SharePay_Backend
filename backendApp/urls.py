from django.urls import path
from . import views

urlpatterns = [
   path('', views.defaultViews, name='default'),
   path('prueba1/', views.hello_world, name='hello_world'),
   path('link2/', views.vistas, name='vistas')
]