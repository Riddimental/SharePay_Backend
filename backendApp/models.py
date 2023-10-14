from django.db import models

class Usuarios(models.Model):
    UserID = models.AutoField(primary_key=True)
    CorreoElectronico = models.CharField(max_length=255, unique=True)
    NombreCompleto = models.CharField(max_length=255)
    Apodo = models.CharField(max_length=255)
    FotoOAvatar = models.CharField(max_length=512)
    Estado = models.CharField(max_length=10)

class Contactos(models.Model):
    ContactID = models.AutoField(primary_key=True)
    UserID = models.IntegerField()
    CorreoElectronico = models.CharField(max_length=255)

class Eventos(models.Model):
    EventoID = models.AutoField(primary_key=True)
    Creador = models.IntegerField()
    Nombre = models.CharField(max_length=255)
    Descripcion = models.TextField(null=True, blank=True)
    Tipo = models.CharField(max_length=10)
    FotoOAvatar = models.CharField(max_length=512, null=True, blank=True)

class ParticipantesEvento(models.Model):
    ParticipanteID = models.AutoField(primary_key=True)
    UserID = models.IntegerField()
    EventoID = models.IntegerField()
    Estado = models.CharField(max_length=10)

class Actividades(models.Model):
    ActividadID = models.AutoField(primary_key=True)
    EventoID = models.IntegerField()
    Creador = models.IntegerField()
    Descripcion = models.TextField()
    ValorTotal = models.DecimalField(max_digits=10, decimal_places=2)

class ParticipantesActividad(models.Model):
    ActividadParticipanteID = models.AutoField(primary_key=True)
    ActividadID = models.IntegerField()
    UserID = models.IntegerField()
    PorcentajeParticipacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ValorFijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Saldos(models.Model):
    SaldoID = models.AutoField(primary_key=True)
    EventoID = models.IntegerField()
    UserID = models.IntegerField()
    TotalDeuda = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPago = models.DecimalField(max_digits=10, decimal_places=2)

class Pagos(models.Model):
    PagoID = models.AutoField(primary_key=True)
    DeudorUserID = models.IntegerField()
    AcreedorUserID = models.IntegerField()
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    FechaPago = models.DateField()

# Definición de relaciones
class Contactos(models.Model):
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='contactos_usuario')
    CorreoElectronico = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='contactos_correo')
    
class ParticipantesEvento(models.Model):
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    
class ParticipantesActividad(models.Model):
    ActividadID = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    
class Saldos(models.Model):
    EventoID = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    UserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    
class Pagos(models.Model):
    DeudorUserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='pagos_deudor')
    AcreedorUserID = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='pagos_acreedor')
