from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Cliente(models.Model):
    idusuario = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    rut = models.CharField(max_length=12, null=False)
    direccion = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50, null=False)
    telefono = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    valor_unit = models.IntegerField(null=False)
    descripcion = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(
        upload_to='media/images', default='producto_default.png')
    stock = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.nombre


class Wishlist(models.Model):
    idcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_wishlist = models.CharField(max_length=45)
    fecha = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='ProductoWishlist')

    def __str__(self):
        return str(self.nombre_wishlist)

    def total_productos(self):
        cantidad = 0
        producto_wishlists = ProductoWishlist.objects.filter(idwishlist=self)
        for producto in producto_wishlists:
            cantidad += producto.cantidad_deseada
        return cantidad

    def valor_total(self):
        total = 0
        producto_wishlists = ProductoWishlist.objects.filter(idwishlist=self)
        for producto_wishlist in producto_wishlists:
            valor = producto_wishlist.cantidad_deseada * \
                producto_wishlist.idproducto.valor_unit
            total += valor
        return total


class ProductoWishlist(models.Model):
    idwishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    idproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_deseada = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return f"Wishlist: {self.idwishlist} - {self.idwishlist.idcliente.nombre}"

    def valor_total(self):
        return self.cantidad_deseada * self.idproducto.valor_unit


class Pedido(models.Model):
    METODOPAGO_CHOICES = [
        ('Transferencia', 'Transferencia'),
        ('Tarjeta de Credito', 'Tarjeta de Crédito'),
        ('Tarjeta de Debito', 'Tarjeta de Débito')
    ]
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En preparacion', 'En preparación'),
        ('Entregado', 'Entregado'),
        ('En Despacho', 'En Despacho'),
        ('Cancelado', 'Cancelado'),
    ]

    wishlist = models.ForeignKey(
        Wishlist, null=True, blank=True, on_delete=models.SET_NULL)
    fecha = models.DateField(auto_now_add=True)
    direccion_despacho = models.CharField(max_length=100)
    fecha_despacho = models.DateTimeField(null=False)
    subtotal = models.PositiveIntegerField(null=False)
    valordespacho = models.PositiveIntegerField(null=False)
    valortotal = models.PositiveIntegerField(null=False)
    metododepago = models.CharField(
        null=False, max_length=50, choices=METODOPAGO_CHOICES)
    estadopedido = models.CharField(
        null=False, max_length=50, choices=ESTADO_CHOICES)

    def __str__(self):
        return str(self.id)


class Detalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    productos = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(null=False)
    valor_unit = models.PositiveIntegerField(null=False)

    def cantidad_valor(self):
        return self.cantidad * self.valor_unit

    def __str__(self):
        return f"Detalle - Pedido: {self.pedido}, Producto: {self.productos}"
