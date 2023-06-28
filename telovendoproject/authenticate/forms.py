from django import forms
from django.contrib.auth.forms import AuthenticationForm


class FormularioLogin(AuthenticationForm):
    username = forms.CharField(max_length=50, required=True, label='Nombre de Usuario', error_messages={
                               'required': 'El usuario es obligatorio'})
    password = forms.CharField(max_length=16, required=True, label='Contraseña',
                               widget=forms.PasswordInput, error_messages={'required': 'La contraseña es obligatoria'})
