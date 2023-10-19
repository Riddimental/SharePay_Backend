from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'registro', views.register, 'registro')

urlpatterns = [
   path('', views.defaultViews, name='default'),
   path('prueba1/', views.hello_world, name='hello_world'),
   path('link2/', views.vistas, name='vistas'),
   path('registro/', views.register, name='vistas'),
   path('docs/', include_docs_urls(title="API")) 
]