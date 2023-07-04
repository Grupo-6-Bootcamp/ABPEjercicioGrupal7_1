from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido, ProductoWishlist, Wishlist, Detalle
from .forms import ClienteForm, EstadoPedidoForm, ProductoForm, ProductoWishlistForm, WishlistForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum



def index(request):
    return render(request, "index.html")

@method_decorator(staff_member_required, name='dispatch')
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


class CrearClienteView(View):
    template_name = 'crear_cliente.html'

    def get(self, request):
        form = ClienteForm()
        wishlist_form = WishlistForm()
        context = {'form': form, 'wishlist_form': wishlist_form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ClienteForm(request.POST)
        wishlist_form = WishlistForm(request.POST)
        
        if form.is_valid() and wishlist_form.is_valid():
            cliente = form.save()
            wishlist = wishlist_form.save(commit=False)
            wishlist.idcliente = cliente
            wishlist.save()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist.id)

        context = {'form': form, 'wishlist_form': wishlist_form}
        return render(request, self.template_name, context)
    


class AgregarProductosWishlistView(View):
    template_name = 'agregar_productos_wishlist.html'

    def get(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        productos_wishlist = ProductoWishlist.objects.filter(idwishlist=wishlist)

        # Cálculo del valor de despacho
        valordespacho = 0
        for producto_wishlist in productos_wishlist:
            valordespacho += producto_wishlist.idproducto.valor_unit

        form = ProductoWishlistForm()
        context = {'form': form, 'wishlist': wishlist, 'productos_wishlist': productos_wishlist, 'valordespacho': valordespacho}
        return render(request, self.template_name, context)

    def post(self, request, wishlist_id):
        if 'delete' in request.POST:
            product_id = request.POST.get('delete')
            ProductoWishlist.objects.filter(id=product_id).delete()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist_id)

        form = ProductoWishlistForm(request.POST)
        if form.is_valid():
            producto_wishlist = form.save(commit=False)
            wishlist = Wishlist.objects.get(id=wishlist_id)
            producto_wishlist.idwishlist = wishlist
            producto_wishlist.save()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist_id)

        wishlist = Wishlist.objects.get(id=wishlist_id)
        productos_wishlist = ProductoWishlist.objects.filter(idwishlist=wishlist)

        context = {'form': form, 'wishlist': wishlist, 'productos_wishlist': productos_wishlist}
        return render(request, self.template_name, context)
    
