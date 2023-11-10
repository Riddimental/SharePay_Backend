from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework.authtoken import views as tokenviews
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'Perfiles', views.PerfilView , 'Usuarios')
router.register(r'Contactos', views.ContactosView, 'Contactos')
router.register(r'Eventos', views.EventosView, 'Eventos')
router.register(r'ParticipantesEvento', views.ParticipantesEventoView, 'ParticipantesEvento')
router.register(r'Actividades', views.ActividadesView, 'Actividades')
router.register(r'ParticipantesActividad', views.ParticipantesActividadView, 'ParticipantesActividad')
router.register(r'Saldos', views.SaldosView, 'Saldos')
router.register(r'Pagos', views.PagosView, 'Pagos')


urlpatterns = [
   path('log-in/', views.LogInView.as_view()),
   path('log-out/', views.LogOutView.as_view()),
   path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
   path('api/v1/', include(router.urls)),
   path("docs/", include_docs_urls(title='Backend API')),
   path('', views.defaultViews, name='default'), 
   path('generate_token/', tokenviews.obtain_auth_token),
   path('get_user_id/', views.get_user_by_username, name='get user id'),
   path('get_user_info/<str:username>/', GetUser.as_view(), name='get user info'),
]