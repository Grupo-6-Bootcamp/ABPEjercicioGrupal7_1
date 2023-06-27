from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import View
from .forms import FormularioLogin
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('Home')
            form.add_error(
                'password', 'Nombre de usuario o contraseña incorrectos. Porfavor ingrese nuevamente')
            return render(request, self.template_name, {"form": form})
        else:
            return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name='dispatch')
class CerrarSesion(View):
    def get(self, request):
        logout(request)
        return redirect('index')
