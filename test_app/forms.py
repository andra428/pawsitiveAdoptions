from django import forms
from .models import Pet2, CustomUser

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet2
        fields = ['path','name','race','age','health']

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [ 'last_name','first_name', 'email', 'phone','password', 'role', 'animal', 'race', 'size','hair', 'gender', 'age','description']
