from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido
from .forms import EstadoPedidoForm, ProductoForm

def index(request):
    return render(request, "index.html")

class PedidosView(View):
    template_name='pedidos.html'

    def get(self, request, *args, **kwargs):
       pedidos = Pedido.objects.all()
       context = {'pedidos': pedidos}
       return render(request, self.template_name, context=context)

class GestionProdView(View):
   template_name='gestion_prod.html'

   def get(self, request, *args, **kwargs):
      productos = Producto.objects.all()
      context = {'productos': productos}
      return render(request, self.template_name, context=context)
   

class PedidoDetalleView(View):
    template_name: 'detalle_pedido.html'
    

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = EstadoPedidoForm(instance = pedido)
        context = {'pedido' : pedido,
                   "form" : form}
        return render(request, 'detalle_pedido.html', context)

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = EstadoPedidoForm(request.POST, instance = pedido)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.estadopedido = form.cleaned_data['estadopedido']
            pedido.save()
            return redirect('pedidos')

class IngresoProductoView(View):
    template_name = 'nuevo_producto.html'

    def get(self, request):
        form = ProductoForm
        context = {'form' : form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('gestionprod')

def test01(request):

    return render(request, "ecommerce/ecommerce.html")