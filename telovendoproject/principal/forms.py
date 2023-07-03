from django import forms
from .models import Pedido, Producto

class EstadoPedidoForm(forms.ModelForm):
    
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