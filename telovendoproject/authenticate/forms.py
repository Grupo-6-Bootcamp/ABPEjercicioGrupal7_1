from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

# REQUISITO EJERCICIO GRUPAL 3
class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30,
        help_text='Requerido. 30 caracteres o menos. Letras y números solamente.',
        label='Nombre de usuario'
    )

    email = forms.EmailField(
        max_length=254,
        help_text='Requerido. Ingrese una dirección de correo válida.'
    )

    email2 = forms.EmailField(
        max_length=254,
        help_text='Requerido. Ingrese una dirección de correo válida.',
        label='Confirmar correo electrónico'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email2 = cleaned_data.get('email2')

        if email != email2:
            raise forms.ValidationError(
                'Los correos electrónicos no coinciden. Por favor, inténtelo de nuevo.')

    class Meta:
        model = User
        fields = ('username', 'email', 'email2')


class FormularioLogin(AuthenticationForm):
    email = forms.CharField(max_length=50, required=True, label='Correo Electrónico', error_messages={
        'required': 'El correo electrónico es obligatorio'})
    password = forms.CharField(max_length=16, required=True, label='Contraseña',
                               widget=forms.PasswordInput, error_messages={'required': 'La contraseña es obligatoria'})
    class Meta:
        model = User
