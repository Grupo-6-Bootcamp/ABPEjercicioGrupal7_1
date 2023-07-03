from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import PedidosView, GestionProdView, PedidoDetalleView, IngresoProductoView, test01

urlpatterns = [
    path('', views.index, name='index'),
    path('pedidos', PedidosView.as_view(), name='pedidos'),
    path('gestion', GestionProdView.as_view(), name="gestionprod"),
    path('pedido_detalle/<int:pk>/', PedidoDetalleView.as_view(), name="pedido_detalle"),
    path('nuevo_producto', IngresoProductoView.as_view(), name="nuevo_producto"),
    path('test01/', views.test01, name='test01'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
