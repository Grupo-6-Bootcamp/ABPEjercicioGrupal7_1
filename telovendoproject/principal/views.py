from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido

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