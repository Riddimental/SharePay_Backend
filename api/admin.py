from django.contrib import admin
from .models import Perfil, Contactos, Eventos, ParticipantesEvento, Actividades, ParticipantesActividad, Saldos, Pagos


# Register your models here.
#admin.site.register(Usuarios)
admin.site.register(Perfil)
admin.site.register(Contactos)
admin.site.register(Eventos)
admin.site.register(ParticipantesEvento)
admin.site.register(Actividades)
admin.site.register(ParticipantesActividad)
admin.site.register(Saldos)
admin.site.register(Pagos)
