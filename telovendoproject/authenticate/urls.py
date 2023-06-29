from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CerrarSesion.as_view(), name='logout'),
    # REQUISITO EJERCICIO GRUPAL 3
    # path('register/', views.Registro.as_view(), name='register'),
]
