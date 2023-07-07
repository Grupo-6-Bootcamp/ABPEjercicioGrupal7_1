from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('pedidos', PedidosView.as_view(), name='pedidos'),
    path('gestion', GestionProdView.as_view(), name="gestionprod"),
    path('pedido_detalle/<int:pk>/',
         PedidoDetalleView.as_view(), name="pedido_detalle"),
    path('nuevo_producto', IngresoProductoView.as_view(), name="nuevo_producto"),
    path('test01/', views.test01, name='test01'),
    path('wishlist/', WishList.as_view(), name="wishlist"),
    path('crear_cliente/', CrearClienteView.as_view(), name="crear_cliente"),
    path('agregar_productos_wishlist/<int:wishlist_id>/',
         AgregarProductosWishlistView.as_view(), name="agregar_productos_wishlist"),
    path('crear_pedido/', CrearPedidoView.as_view(), name="crear_pedido"),
    path('panel_usuario/', PanelUsuario.as_view(), name="panel_usuario"),
    path('productos', ProductList.as_view(), name='productos'),
    path('producto/<int:id>/', ProductDetail.as_view(), name='producto'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
