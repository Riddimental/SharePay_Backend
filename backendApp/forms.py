from django import forms
from .models import Usuarios, Passwords

class UserForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = ['UserID', 'CorreoElectronico', 'NombreCompleto', 'Apodo', 'FotoOAvatar', 'Estado']
      
class PasswordsForm(forms.ModelForm):
    class Meta:
        model = Passwords
        fields = ['Password']