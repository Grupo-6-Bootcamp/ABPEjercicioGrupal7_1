from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Cliente(models.Model):
    idusuario = models.ForeignKey(User, on_delete=models.CASCADE)
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
    imagen = models.ImageField(upload_to='media/images', default='producto_default.png')
    stock = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.nombre

class Wishlist(models.Model):
    idcliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    fecha = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='ProductoWishlist')

    def __str__(self):
        return self.nombre

class ProductoWishlist(models.Model):
    idwishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    idproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_deseada = models.PositiveIntegerField(blank=False)

    class Meta:
        unique_together = ('idwishlist', 'idproducto')

    def __str__(self):
        return f"Wishlist: {self.idwishlist} - {self.idwishlist.nombre}"


class Pedido(models.Model):
    METODOPAGO_CHOICES = [
        ('Transferencia', 'Transferencia'),
        ('Tarjeta de Credito','Tarjeta de Crédito'),
        ('Tarjeta de Debito', 'Tarjeta de Débito')
    ]
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En preparacion','En preparación'),
        ('Entregado','Entregado'),
        ('En Despacho','En Despacho'),
    ]

    wishlist_idwishlist = models.ForeignKey(Wishlist, null=True, on_delete=models.SET_NULL)
    fecha = models.DateField(auto_now_add=True)
    direccion_despacho = models.CharField(100)
    fecha_despacho = models.DateTimeField(null=False)
    subtotal = models.PositiveIntegerField(null=False)
    valordespacho = models.PositiveIntegerField(null=False)
    valortotal = models.PositiveIntegerField(null=False)
    metododepago = models.CharField(null=False, max_length=50, choices=METODOPAGO_CHOICES)
    estadopedido = models.CharField(null=False, max_length=50, choices=ESTADO_CHOICES)

    def __str__(self):
        return self.idcliente


class Detalle(models.Model):
    pedido_idpedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    productos_idproducto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(null=False)
    valor_unit = models.PositiveIntegerField(null=False)

    class Meta:
        unique_together = ('pedido_idpedido', 'productos_idproducto')

    def __str__(self):
        return f"Detalle - Pedido: {self.pedido_idpedido}, Producto: {self.productos_idproducto}"