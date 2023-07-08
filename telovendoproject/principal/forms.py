from django import forms
from .models import Cliente, Pedido, Producto, Wishlist, ProductoWishlist


class EstadoPedidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EstadoPedidoForm, self).__init__(*args, **kwargs)
        self.fields['estadopedido'].widget.attrs['class'] = 'form-select'

    class Meta():
        model = Pedido
        fields = ('estadopedido',)


class ProductoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = 'Nombre'
        self.fields['valor_unit'].label = 'Valor unitario'
        self.fields['descripcion'].label = 'Descripción'
        self.fields['imagen'].label = 'Imagen'
        self.fields['stock'].label = 'Stock'

        self.fields['nombre'].widget.attrs['class'] = 'form-control'
        self.fields['valor_unit'].widget.attrs['class'] = 'form-control'
        self.fields['descripcion'].widget.attrs['class'] = 'form-control'
        self.fields['imagen'].widget.attrs['class'] = 'form-control'
        self.fields['stock'].widget.attrs['class'] = 'form-control'

    class Meta():
        model = Producto
        fields = '__all__'


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'rut', 'email',
                  'direccion', 'telefono']
        labels = {
            'direccion': 'Dirección de Facturación',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'})
        }


class ClienteExternoForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'rut', 'email',
                  'direccion', 'telefono']
        labels = {
            'direccion': 'Dirección de Facturación',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'telefono': forms.TextInput(attrs={'class': 'form-control'})
        }


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['nombre_wishlist']


class ProductoWishlistForm(forms.ModelForm):
    class Meta:
        model = ProductoWishlist
        exclude = ['idwishlist']


class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ['direccion_despacho', 'metododepago',]


# class Pedido(models.Model):
#     METODOPAGO_CHOICES = [
#         ('Transferencia', 'Transferencia'),
#         ('Tarjeta de Credito', 'Tarjeta de Crédito'),
#         ('Tarjeta de Debito', 'Tarjeta de Débito')
#     ]
#     ESTADO_CHOICES = [
#         ('Pendiente', 'Pendiente'),
#         ('En preparacion', 'En preparación'),
#         ('Entregado', 'Entregado'),
#         ('En Despacho', 'En Despacho'),
#     ]

    # wishlist = models.ForeignKey(
    #     Wishlist, null=True, blank=True, on_delete=models.SET_NULL)
    # fecha = models.DateField(auto_now_add=True)
    # direccion_despacho = models.CharField(max_length=100)
    # fecha_despacho = models.DateTimeField(null=False)
    # subtotal = models.PositiveIntegerField(null=False)
    # valordespacho = models.PositiveIntegerField(null=False)
    # valortotal = models.PositiveIntegerField(null=False)
    # metododepago = models.CharField(
    #     null=False, max_length=50, choices=METODOPAGO_CHOICES)
    # estadopedido = models.CharField(
    #     null=False, max_length=50, choices=ESTADO_CHOICES)

    # def __str__(self):
    #     return str(self.id)
