from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class Usuarios(models.Model):
    UserID = models.AutoField(primary_key=True)
    CorreoElectronico = models.EmailField(unique=True)
    NombreCompleto = models.CharField(max_length=255)
    Apodo = models.CharField(max_length=255)
    
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
        null=True,
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
        return self.CorreoElectronico
    '''
    
    def set_password(self, raw_password):
        # Genera un hash de la contraseña
        self.password = make_password(raw_password)
        # Crea una instancia de Password para almacenar la contraseña
        Passwords.objects.create(UserID=self, Password=self.password)
    '''
    

'''
al crear un usuario debe hacer:

user = Usuarios(UserID='admin', CorreoElectronico='admin@example.com', NombreCompleto='admin', Apodo='admin', FotoOAvatar=, Estado )
user.set_password('password123')  # Define la contraseña del usuario
user.save()  # Guarda el superusuario en la base de datos
'''

class Passwords(models.Model):
    PasswordID = models.AutoField(primary_key=True)
    CorreoElectronico = models.OneToOneField(Usuarios, to_field='CorreoElectronico', on_delete=models.CASCADE)
    Password = models.CharField(max_length=128)
    Creado_en = models.DateTimeField(auto_now_add=True)
    #Pregunta_Seguridad = models.CharField(max_length=255)
    #Respuesta = models.CharField(max_length=255)
    
    def set_password(self, raw_password):
        self.Password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.Password)

    def __str__(self):
        return f" For {self.UserID.Apodo}"

class Contactos(models.Model):
    ContactID = models.AutoField(primary_key=True)
    Contacto_de = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='contactos_usuario')
    Contacto = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='contactos_correo')

class Eventos(models.Model):
    EventoID = models.AutoField(primary_key=True)
    Creador = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
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
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
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
    Creador = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    Descripcion = models.TextField()
    ValorTotal = models.DecimalField(max_digits=10, decimal_places=2)

class ParticipantesActividad(models.Model):
    ActividadParticipanteID = models.AutoField(primary_key=True)
    ActividadID = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    PorcentajeParticipacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ValorFijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Saldos(models.Model):
    SaldoID = models.AutoField(primary_key=True)
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    TotalDeuda = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPago = models.DecimalField(max_digits=10, decimal_places=2)

class Pagos(models.Model):
    PagoID = models.AutoField(primary_key=True)
    DeudorUserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='deudor_usuario')
    AcreedorUserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='acreedor_ususario')
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    FechaPago = models.DateField()
