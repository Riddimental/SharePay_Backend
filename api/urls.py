from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework.authtoken import views as tokenviews
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'Perfiles', views.PerfilView , 'Perfiles')
router.register(r'Contactos', views.ContactosView, 'Contactos')
router.register(r'Eventos', views.EventosView, 'Eventos')
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
   path('get_user/', views.get_user, name='get user information'),
   path('get_contacts/', views.get_user_contacts, name='get contacts information'),
   path('get_participants/', views.get_participants, name='get participants information'),
   path('get_event_activities/', views.get_event_activities, name='get activities from a selected event'),
   path('get_all_events/', views.get_user_events, name='get events information'),
   path('have_common_events/', views.have_common_events, name='get list of common events'),
   path('update_user/', views.UpdateUserView.as_view(), name='update user information'),
   path('update_contactos/', views.UpdateContactsView.as_view(), name='update contacts information'),
   path('update_event/', views.UpdateEventView.as_view(), name='update Event information'),
   path('delete_contactos/', views.DeleteContactsView.as_view(), name='delete contacts information'),
   path('delete_event/', views.DeleteEventView.as_view(), name='delete contacts information'),
   path('create_contactos/', views.CreateContactsView.as_view(), name='Create contacts'),
   path('create_events/', views.CreateEventsView.as_view(), name='Create events'),
   path('update_perfil/', views.UpdateProfileView.as_view(), name='update perfil'),
]

