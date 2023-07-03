from django.contrib import admin
from .models import Cliente, Producto, Wishlist, Pedido, Detalle, ProductoWishlist
# Register your models here.
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Wishlist)
admin.site.register(ProductoWishlist)
admin.site.register(Pedido)
admin.site.register(Detalle)