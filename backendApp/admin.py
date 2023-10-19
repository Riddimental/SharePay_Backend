from django.contrib import admin
from .models import Usuarios, Contactos, Eventos, ParticipantesEvento, Actividades, ParticipantesActividad, Saldos, Pagos, Passwords
from .forms import UserForm

import re

class PasswordInline(admin.StackedInline):
    model = Passwords
    extra = 0
    min_num = 1
    validate_min = True
    can_delete = False


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    inlines = [PasswordInline]

# Register your models here.
#admin.site.register(Usuarios)
admin.site.register(Usuarios, UserAdmin)
admin.site.register(Contactos)
admin.site.register(Eventos)
admin.site.register(ParticipantesEvento)
admin.site.register(Actividades)
admin.site.register(ParticipantesActividad)
admin.site.register(Saldos)
admin.site.register(Pagos)
#admin.site.register(Passwords)
