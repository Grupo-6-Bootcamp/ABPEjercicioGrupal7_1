from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import logout, login, authenticate
from .form import SignUpForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import FormularioLogin
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.

class LoginView(View):
    template_name = "registration/login.html"

    def get(self, request):
        context = {'formulario_login': FormularioLogin()}
        return render(request, "registration/login.html", context)

    def post(self, request):
        usuario = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            context = {"error": "Usuario no encontrado",
                       'formulario_login': FormularioLogin()}
            return render(request, 'registration/login.html', context)


@method_decorator(login_required, name='dispatch')
class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class SignUp(View):
    def get(self, request):
        formulario = SignUpForm()
        context = {'formulario': formulario}
        return render(request, 'registration/signup.html', context)

    def post(self, request):
        formulario = SignUpForm(request.POST)
        if formulario.is_valid():
            user = SignUpForm(request.POST)
            user.is_active = False
            user.set.username(formulario.cleaned_data['username'])
            user.set.email(formulario.cleaned_data['email'])
            user.set.email2(formulario.cleaned_data['email2'])
            user.save()

            random_pass = User.objects.make_random_password()

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta de TeLoVendo'
            message = render_to_string('registration/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'password': random_pass,
            })
            print(f'Email enviado a: , {user.email}')
            send_mail(mail_subject, message,
                      settings.EMAIL_HOST_USER, [user.email])
            user = authenticate(username=user.username, password=random_pass)
            login(request, user)
            return redirect('index')

        else:
            print(formulario.errors)
            context = {'formulario': formulario}
            return render(request, 'registration/signup.html', context)


class ActivarCuenta(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('index')
        else:
            return render(request, 'registration/activate_account_invalid.html')
