from django.contrib.auth.models import User
from django.db import models
##from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password

class profile(models.Model):
    apodo: models.OneToOneRel(User, to='username',field_name='perfil', on_delete=models.CASCADE)
    avatar: models.CharField(max_length=255)
    OPCIONES_FOTO_AVATAR = [
        ('https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png',"avatar 1"),
        ('https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png',"avatar 2"),
        ('https://cdn3.iconfinder.com/data/icons/business-avatar-1/512/11_avatar-512.png', "avatar 3"),
        ('https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', "avatar 4"),
        ('https://as1.ftcdn.net/v2/jpg/01/21/93/74/1000_F_121937450_E3o8jRG3mKbMaAFprSuNOlyrLraSVVua.jpg',"avatar 5"),
        ('https://banner2.cleanpng.com/20180625/req/kisspng-computer-icons-avatar-business-computer-software-user-avatar-5b3097fcae25c3.3909949015299112927133.jpg', "avatar 6")
    ]
    
    FotoOAvatar = models.CharField(
        max_length=225,
        choices=OPCIONES_FOTO_AVATAR,
        default='https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png'
    )
    
    def __str__(self):
        return self.apodo

class Usuarios(models.Model):#modelo obsoleto de Usuarios, ahora usamos el de Django
    UserID = models.AutoField(primary_key=True)
    CorreoElectronico = models.EmailField(unique=True)
    NombreCompleto = models.CharField(max_length=255)
    Apodo = models.CharField(max_length=255)
    # user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    
    OPCIONES_FOTO_AVATAR = [
        ('https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png',"avatar 1"),
        ('https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper-thumbnail.png',"avatar 2"),
        ('https://cdn3.iconfinder.com/data/icons/business-avatar-1/512/11_avatar-512.png', "avatar 3"),
        ('https://static.vecteezy.com/system/resources/previews/019/896/008/original/male-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png', "avatar 4"),
        ('https://as1.ftcdn.net/v2/jpg/01/21/93/74/1000_F_121937450_E3o8jRG3mKbMaAFprSuNOlyrLraSVVua.jpg',"avatar 5"),
        ('https://banner2.cleanpng.com/20180625/req/kisspng-computer-icons-avatar-business-computer-software-user-avatar-5b3097fcae25c3.3909949015299112927133.jpg', "avatar 6")
    ]
    
    FotoOAvatar = models.CharField(
        max_length=225,
        choices=OPCIONES_FOTO_AVATAR,
        default='https://static.vecteezy.com/system/resources/previews/019/896/012/original/female-user-avatar-icon-in-flat-design-style-person-signs-illustration-png.png'
    )
    
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]
    
    Estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='activo'  # activo por defecto
    )
    
    def __str__(self):
        return self.Apodo

class Passwords(models.Model):#aqui ya no se almacenan las contraseñas.
    UserID = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    Password = models.CharField(max_length=128)
    Creado_en = models.DateTimeField(auto_now_add=True)
    #Pregunta_Seguridad = models.CharField(max_length=255)
    #Respuesta = models.CharField(max_length=255)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f" For {self.UserID.Apodo}"

class Contactos(models.Model):
    ContactID = models.AutoField(primary_key=True)
    Contacto_de = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='contactos_usuario')#el que agrega el contacto
    Contacto = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='contactos_correo')#el agregado

class Eventos(models.Model):
    EventoID = models.AutoField(primary_key=True)
    Creador = models.ForeignKey(profile, on_delete=models.CASCADE)
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
    
    FotoOAvatar = models.CharField(max_length=225)

class ParticipantesEvento(models.Model):
    ParticipanteID = models.AutoField(primary_key=True)
    Apodo = models.ForeignKey(profile, on_delete=models.CASCADE)
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

class Actividades(models.Model):
    ActividadID = models.AutoField(primary_key=True)
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    Creador = models.ForeignKey(profile, on_delete=models.CASCADE)
    Descripcion = models.TextField()
    ValorTotal = models.DecimalField(max_digits=10, decimal_places=2)

class ParticipantesActividad(models.Model):
    ActividadParticipanteID = models.AutoField(primary_key=True)
    ActividadID = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    Apodo = models.ForeignKey(profile, on_delete=models.CASCADE)
    PorcentajeParticipacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ValorFijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Saldos(models.Model):
    SaldoID = models.AutoField(primary_key=True)
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    Apodo = models.ForeignKey(profile, on_delete=models.CASCADE)
    TotalDeuda = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPago = models.DecimalField(max_digits=10, decimal_places=2)

class Pagos(models.Model):
    PagoID = models.AutoField(primary_key=True)
    Deudor = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='deudor_usuario')
    Acreedor = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='acreedor_ususario')
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    FechaPago = models.DateField()
