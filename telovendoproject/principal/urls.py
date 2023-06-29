from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import PedidosView, GestionProdView

urlpatterns = [
    path('', views.index, name='index'),
    path('pedidos', PedidosView.as_view(), name='pedidos'),
    path('gestion', GestionProdView.as_view(), name="gestionprod"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
