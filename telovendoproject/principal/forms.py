from django import forms
from .models import Cliente, Pedido, Producto, Wishlist, ProductoWishlist, Detalle
import datetime


# class EstadoPedidoForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(EstadoPedidoForm, self).__init__(*args, **kwargs)
#         self.fields['estadopedido'].widget.attrs['class'] = 'form-select'

#     class Meta():
#         model = Pedido
#         fields = ('estadopedido',)

class EstadoPedidoForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        user = request.user
        if user.is_superuser or user.is_staff:
            super(EstadoPedidoForm, self).__init__(*args, **kwargs)
            self.fields['estadopedido'].widget.attrs['class'] = 'form-select'
        else:
            super(EstadoPedidoForm, self).__init__(*args, **kwargs)
            self.fields['estadopedido'].widget.attrs['class'] = 'form-select'
            self.fields['estadopedido'].widget.attrs['disabled'] = True

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

class PedidoExternoForm(forms.ModelForm):
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
            'estadopedido': forms.TextInput(attrs={'class': 'form-control'})
        }

class PedidoUsuarioForm(forms.ModelForm):
    fecha_despacho = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control',
                'placeholder': 'Fecha',
                'type': 'date',
                'readonly': True,
            }
        ),
        initial=datetime.timedelta(days=9) + datetime.date.today()
    )

    direccion_despacho = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    subtotal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    valordespacho = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True,}), required=False)
    valortotal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}), required=False)
    metododepago = forms.Select(attrs={'class': 'form-control'})
    estadopedido = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'value': 'Pendiente'}), required=False)

    class Meta:
        model = Pedido
        fields = ['direccion_despacho', 'fecha_despacho', 'subtotal', 'valordespacho', 'valortotal', 'metododepago', 'estadopedido']


# class DetalleForm(forms.ModelForm):
#     class Meta:
#         model = Detalle
#         fields = ['producto', 'cantidad']
#         widgets = {
#             'producto': forms.Select(attrs={'class': 'form-control'}),
#             'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
#         }
# 


class AgregarProductoForm(forms.Form):
    wishlist = forms.ModelChoiceField(queryset=None, label='Seleccionar Wishlist')
    cantidad = forms.IntegerField(min_value=1, label='Cantidad deseada')

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)
        if cliente:
            self.fields['wishlist'].queryset = Wishlist.objects.filter(idcliente=cliente)
