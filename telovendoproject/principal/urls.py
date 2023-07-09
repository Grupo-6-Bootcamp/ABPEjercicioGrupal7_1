from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('pedidos', PedidosView.as_view(), name='pedidos'),
    path('gestion', GestionProdView.as_view(), name="gestionprod"),
    path('nuevo_producto', IngresoProductoView.as_view(), name="nuevo_producto"),
    path('test01/', views.test01, name='test01'),
    path('wishlist/', WishList.as_view(), name="wishlist"),
    path('crear_cliente/', CrearClienteView.as_view(), name="crear_cliente"),
    path('agregar_productos_wishlist/<int:wishlist_id>/', AgregarProductosWishlistView.as_view(), name="agregar_productos_wishlist"),
    path('crear_pedido/<int:wishlist_id>/<int:cliente_id>/', CrearPedidoView.as_view(), name='crear_pedido'),
    path('panel_usuario/', PanelUsuario.as_view(), name="panel_usuario"),
    path('productos', ProductList.as_view(), name='productos'),
    path('producto/<int:pk>/', ProductDetail.as_view(), name='producto'),
    path('contacto/', ContactView.as_view(), name="contacto"),

# Grupal 5: vistas para crear el pedido del usuario registrado

    #path('pedido_cliente', CreatePedidoView.as_view(), name='pedido_cliente'),
    #path('detalle/<int:pedido_id>/', views.DetallePedidoView.as_view(), name='detalle_pedido'),
    #path('carrito/', views.CarritoCompraView.as_view(), name='carrito_compra'),
    #path('confirmar/', views.ConfirmarCompraView.as_view(), name='confirmar_compra'),
    #path('pago/', views.MetodoPagoView.as_view(), name='metodo_pago'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()