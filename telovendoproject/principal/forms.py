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
        fields = ['nombre', 'apellido', 'rut', 'direccion', 'email', 'telefono']


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['nombre']

class ProductoWishlistForm(forms.ModelForm):
    class Meta:
        model = ProductoWishlist
        exclude = ['idwishlist']
