from django import forms
from .models import Cliente, Pedido, Producto, Wishlist, ProductoWishlist, Detalle


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
        widgets = {
            'nombre_wishlist': forms.DateInput(attrs={'class': 'form-control'})
        }


class ProductoWishlistForm(forms.ModelForm):
    class Meta:
        model = ProductoWishlist
        exclude = ['idwishlist']


# class DetallePedidoForm(forms.ModelForm):
#     class Meta:
#         model = Pedido
#         fields = ['direccion_despacho', 'metododepago',]

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_despacho', 'fecha_despacho', 'subtotal', 'valordespacho',
                    'valortotal', 'metododepago', 'estadopedido']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control'}),
            'direccion_despacho': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_despacho': forms.DateInput(format=('%Y-%m-%d'), attrs= {'class':'form-control', 'placeholder': 'Fecha', 'type': 'date'}),
            'subtotal': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'valordespacho': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'valortotal': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'metododepago': forms.Select(attrs={'class': 'form-control'}),
            'estadopedido': forms.Select(attrs={'class': 'form-control'})
        }

# class DetalleForm(forms.ModelForm):
#     class Meta:
#         model = Detalle
#         fields = ['producto', 'cantidad']
#         widgets = {
#             'producto': forms.Select(attrs={'class': 'form-control'}),
#             'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
#         }
# 