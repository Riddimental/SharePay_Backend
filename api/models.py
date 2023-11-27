from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.hashers import make_password, check_password
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.Perfil.save()


class Perfil(models.Model):
    user = models.OneToOneField(User, to_field="username", on_delete=models.CASCADE, related_name='Perfil')
    bio = models.TextField(max_length=400, null=True, blank=True)

    OPCIONES_FOTO_AVATAR = [
        ('https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', "avatar 1"),
        ('https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png', "avatar 2"),
        ('https://cdn3.iconfinder.com/data/icons/business-avatar-1/512/11_avatar-512.png', "avatar 3"),
        ('https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', "avatar 4"),
        ('https://as1.ftcdn.net/v2/jpg/01/21/93/74/1000_F_121937450_E3o8jRG3mKbMaAFprSuNOlyrLraSVVua.jpg', "avatar 5"),
        ('https://banner2.cleanpng.com/20180625/req/kisspng-computer-icons-avatar-business-computer-software-user-avatar-5b3097fcae25c3.3909949015299112927133.jpg', "avatar 6")
    ]

    FotoOAvatar = models.CharField(
        max_length=255,
        choices=OPCIONES_FOTO_AVATAR,
        default='https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png'
    )

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['user']


    def __str__(self):
        return self.user.username


class Contactos(models.Model):
    ContactID = models.AutoField(primary_key=True)
    Emisor = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Contacto_emisor')
    Remitente = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Contacto_remitente')
    ESTADO_CHOICES = [('Aceptada', 'Aceptada'), ('Rechazada', 'Rechazada'), ('Pendiente', 'Pendiente'), ('Eliminado', 'Eliminado')]
    Estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def clean(self):
        if not self.Emisor_id or not self.Remitente_id:
            raise ValidationError("Los campos Emisor y Remitente no pueden estar en blanco.")
        if self.Emisor_id == self.Remitente_id:
            raise ValidationError("El Emisor y el Remitente no pueden ser el mismo.")

        # Verificar si el contacto inverso ya existe
        reverse_contact_exists = Contactos.objects.filter(
            Q(Emisor=self.Remitente, Remitente=self.Emisor)
        ).exists()

        if reverse_contact_exists:
            raise ValidationError("El contacto inverso ya existe.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Emisor} invitó a {self.Remitente}"

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['ContactID']
        unique_together = [['Emisor', 'Remitente'], ['Remitente', 'Emisor']]


class Eventos(models.Model):
    EventoID = models.AutoField(primary_key=True)
    Creador = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Eventos_creador')
    Nombre = models.CharField(max_length=255)
    Descripcion = models.TextField(null=True, blank=True)
    
    TIPO_CHOICES = [
        ('viaje', 'Viaje'),
        ('hogar', 'Hogar'),
        ('pareja', 'Pareja'),
        ('comida', 'Comida'),
        ('otro', 'Otro'),
    ]
    
    Tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='otro'  # otro por defecto
    )
    
    OPCIONES_FOTO_AVATAR = [
        ('https://w7.pngwing.com/pngs/980/935/png-transparent-clapperboard-architecture-sports-activities-text-fashion-logo-thumbnail.png', "avatar 1"),
        ('https://png.pngtree.com/png-clipart/20220628/original/pngtree-food-logo-png-image_8239850.png', "avatar 2"),
        ('https://logo.com/image-cdn/images/kts928pd/production/cbe600c9fc90afe063527b300816e390f57a8915-349x346.png', "avatar 3"),
        ('https://assets.stickpng.com/images/590605810cbeef0acff9a63c.png', "avatar 4"),
        ('https://logowik.com/content/uploads/images/google-shopping.jpg', "avatar 5"),
        ('https://png.pngtree.com/png-clipart/20230921/original/pngtree-swimming-logo-logo-pool-white-vector-png-image_12645079.png', "avatar 6")
    ]

    FotoOAvatar = models.CharField(
        max_length=255,
        choices=OPCIONES_FOTO_AVATAR,
        default='https://assets.stickpng.com/images/590605810cbeef0acff9a63c.png'
    )
    
    def __str__(self):
        return f"{self.Creador} creó el evento {self.Nombre}"
    class Meta:
      verbose_name='Evento'
      verbose_name_plural='Eventos'
      ordering=['EventoID']
      
    def save(self, *args, **kwargs):
        # Guardar el evento
        super().save(*args, **kwargs)

        # Verificar si el participante ya existe
        participant_exists = ParticipantesEvento.objects.filter(
            Apodo=self.Creador,
            EventoID=self
        ).exists()

        if not participant_exists:
            # Si no existe, crear el participante
            ParticipantesEvento.objects.create(
                Apodo=self.Creador,
                EventoID=self,
                Estado='activo'
            )

@receiver(post_save, sender=Eventos)
def create_participant(sender, instance, created, **kwargs):
    if created:
        ParticipantesEvento.objects.create(
            Apodo=instance.Creador,
            EventoID=instance,
            Estado='activo'
        )
class ParticipantesEvento(models.Model):
    ParticipanteID = models.AutoField(primary_key=True)
    Apodo = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Eventos_participante')
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    Estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='activo'  # activo por defecto
    )
    
    class Meta:
      verbose_name='Participante del evento'
      verbose_name_plural='Participantes del evento'
      ordering=['ParticipanteID']
      
    def __str__(self):
        return f"{self.Apodo} participará en el evento {self.EventoID.Nombre}"

class Actividades(models.Model):
    ActividadID = models.AutoField(primary_key=True)
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    Creador = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Actividad_creador')
    Descripcion = models.TextField()
    ValorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
      verbose_name='Actividad'
      verbose_name_plural='Actividades'
      ordering=['ActividadID']

class ParticipantesActividad(models.Model):
    ActividadParticipanteID = models.AutoField(primary_key=True)
    ActividadID = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    Apodo = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Actividad_participantes')
    PorcentajeParticipacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ValorFijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
      verbose_name='Participante de actividad'
      verbose_name_plural='Participantes de actividad'
      ordering=['ActividadParticipanteID']

class Saldos(models.Model):
    SaldoID = models.AutoField(primary_key=True)
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    Apodo = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Saldo_para')
    TotalDeuda = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPago = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
      verbose_name='Saldo'
      verbose_name_plural='Saldos'
      ordering=['SaldoID']

class Pagos(models.Model):
    PagoID = models.AutoField(primary_key=True)
    Deudor = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Pagos_deudor')
    Acreedor = models.ForeignKey('Perfil', on_delete=models.CASCADE, to_field="user", related_name='Pagos_acreedor')
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    FechaPago = models.DateField()
    Completado = models.BooleanField(default=False)
    
    class Meta:
      verbose_name='Pago'
      verbose_name_plural='Pagos'
      ordering=['PagoID']
