from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


def index(request):
    return render(request, "index.html")

class PedidosView(TemplateView):
    template_name='pedidos.html'

    def get(self, request, *args, **kwargs):
       result = []
       if not result:
          pass
       context = {}
       return render(request, self.template_name, context=context)
    
class GestionProdView(TemplateView):
    template_name='gestion_prod.html'

    def get(self, request, *args, **kwargs):
       result = []
       if not result:
          pass
       context = {}
       return render(request, self.template_name, context=context)