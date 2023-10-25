from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Usuarios', views.UsuariosView, 'Usuarios')
router.register(r'Passwords', views.PasswordsView, 'Passwords')
router.register(r'Contactos', views.ContactosView, 'Contactos')
router.register(r'Eventos', views.EventosView, 'Eventos')
router.register(r'ParticipantesEvento', views.ParticipantesEventoView, 'ParticipantesEvento')
router.register(r'Actividades', views.ActividadesView, 'Actividades')
router.register(r'ParticipantesActividad', views.ParticipantesActividadView, 'ParticipantesActividad')
router.register(r'Saldos', views.SaldosView, 'Saldos')
router.register(r'Pagos', views.PagosView, 'Pagos')


urlpatterns = [
   path('api/v1/', include(router.urls)),
   path("docs/", include_docs_urls(title='Backend API')),
   path('', views.defaultViews, name='default'),
   path('prueba1/', views.hello_world, name='hello_world'),
   path('link2/', views.vistas, name='vistas'), 
]