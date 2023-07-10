from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
from .views import eliminar_pedido
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pedidos', PedidosView.as_view(), name='pedidos'),
    path('gestion', GestionProdView.as_view(), name="gestionprod"),
    path('nuevo_producto', IngresoProductoView.as_view(), name="nuevo_producto"),
    path('crear_cliente/', CrearClienteView.as_view(), name="crear_cliente"),
    path('agregar_productos_wishlist/<int:wishlist_id>/',
         AgregarProductosWishlistView.as_view(), name="agregar_productos_wishlist"),
    path('crear_pedido/<int:wishlist_id>/<int:cliente_id>/',
         CrearPedidoView.as_view(), name='crear_pedido'),
    path('panel_usuario/', PanelUsuario.as_view(), name="panel_usuario"),
    path('productos', ProductList.as_view(), name='productos'),
    path('producto/<int:pk>/', ProductDetail.as_view(), name='producto'),
    path('contacto/', ContactView.as_view(), name="contacto"),
    path('mis_wishlist/', ListaWishListView.as_view(), name="user_wishlist"),
    path('wishlist_detalle/<int:wishlist_id>/',
         WishlistDetalleView.as_view(), name="wishlist_detalle"),
    path('pedido_detalle/<int:pk>/',
         PedidoDetalleView.as_view(), name="pedido_detalle"),
    path('pedido_usuario/<int:wishlist_id>/<int:cliente_id>',
         CrearPedidoUsuarioView.as_view(), name="pedido_usuario"),
    path('pedido_detalle/<int:pk>/eliminar/',
         eliminar_pedido, name="eliminar_pedido"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
