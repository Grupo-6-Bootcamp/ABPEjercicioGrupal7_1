from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
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

        if email and email2 and email != email2:
            raise forms.ValidationError(
                'Los correos electrónicos no coinciden. Por favor, inténtelo de nuevo.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()  # Establecer una contraseña no utilizable
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'email2')
