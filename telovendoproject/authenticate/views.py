from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from .forms import FormularioLogin
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class LoginView(View):
    template_name = "registration/login.html"

    def get(self, request):
        context = {'formulario_login': FormularioLogin()}
        return render(request, "registration/login.html", context)

    def post(self, request):
        usuario = authenticate(
            request, email=request.POST['email'], password=request.POST['password'])
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            context = {"error": "Usuario no encontrado",
                       'formulario_login': FormularioLogin()}
            print(context)
            return render(request, 'registration/login.html', context)


@method_decorator(login_required, name='dispatch')
class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect('index')

# REQUISITO EJERCICIO GRUPAL 3
#
#class Registro(View):
#    def get(self, request):
#        formulario = SignUpForm(request.POST)
#        context = {'formulario': formulario}
#        template_name = "registration/signup.html"
#        return render(request, template_name, context)
#
#    def post(self, request):
#        formulario = SignUpForm(request.POST)
#        if formulario.is_valid():
#            random_pass = User.objects.make_random_password(
#                length=8, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
#            user = User.objects.create_user(
#                username=formulario.cleaned_data['username'],
#                email=formulario.cleaned_data['email'],
#                password=random_pass)
#            user.is_active = True
#            user.save()
#            send_mail(
#                'Registro en telovendo.cl',
#                'Bienvenido a Telovendo, su contraseña es: ' + random_pass,
#                settings.EMAIL_HOST_USER,
#                (user.email,),
#                fail_silently=False,
#            )
#            print(
#                f'El username {user.username}, cuyo correo es {user.email} tiene la contraseña: {random_pass}')
#            return redirect('login')
#        else:
#            print(formulario.errors)
#            context = {'formulario': formulario}
#            return render(request, 'registration/signup.html', context)
#