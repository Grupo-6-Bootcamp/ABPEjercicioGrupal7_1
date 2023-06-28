from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CerrarSesion.as_view(), name='logout'),
    path('register/', views.SignUp.as_view(), name='register'),
    path('activate/<uidb64>/<token>/',
         views.ActivarCuenta.as_view(), name='activate'),
]
