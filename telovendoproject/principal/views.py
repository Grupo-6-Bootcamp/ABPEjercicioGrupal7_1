from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido, ProductoWishlist, Wishlist, Detalle, Cliente, User
from .forms import ClienteForm, EstadoPedidoForm, ProductoForm, ProductoWishlistForm, WishlistForm, PedidoForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

User = get_user_model()


def index(request):
    return render(request, "index.html")


@method_decorator(staff_member_required, name='dispatch')
class PedidosView(View):
    template_name = 'pedidos.html'

    def get(self, request, *args, **kwargs):
        pedidos = Pedido.objects.all()
        context = {'pedidos': pedidos}
        return render(request, self.template_name, context=context)


class GestionProdView(View):
    template_name = 'gestion_prod.html'

    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        context = {'productos': productos}
        return render(request, self.template_name, context=context)


class PedidoDetalleView(View):
    template_name: 'detalle_pedido.html'

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = EstadoPedidoForm(instance=pedido)
        context = {'pedido': pedido,
                   "form": form}
        return render(request, 'detalle_pedido.html', context)

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = EstadoPedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.estadopedido = form.cleaned_data['estadopedido']
            pedido.save()
            return redirect('pedidos')


class IngresoProductoView(View):
    template_name = 'nuevo_producto.html'

    def get(self, request):
        form = ProductoForm
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('gestionprod')


def test01(request):

    return render(request, "ecommerce/index.html")


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
    subtotal = 0

    def get(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        productos_wishlist = ProductoWishlist.objects.filter(
            idwishlist=wishlist)

        for producto_wishlist in productos_wishlist:
            self.subtotal += producto_wishlist.idproducto.valor_unit * \
                producto_wishlist.cantidad_deseada

        form = ProductoWishlistForm()
        context = {'form': form, 'wishlist': wishlist,
                   'productos_wishlist': productos_wishlist, 'subtotal': self.subtotal}
        return render(request, self.template_name, context)

    def post(self, request, wishlist_id):
        if 'delete' in request.POST:
            product_id = request.POST.get('delete')
            ProductoWishlist.objects.filter(id=product_id).delete()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist_id)

        if 'regresar' in request.POST:
            # cliente = Cliente.objects.get(cliente_id=wishlist.idcliente)
            # context = {'cliente': cliente}
            return redirect('crear_cliente')

        if 'continuar' in request.POST:
            return redirect('crear_pedido', wishlist_id=wishlist_id, subtotal=self.subtotal)
            # def get(self, request, wishlist_id, subtotal):
        form = ProductoWishlistForm(request.POST)
        if form.is_valid():
            producto_wishlist = form.save(commit=False)
            wishlist = Wishlist.objects.get(id=wishlist_id)
            producto_wishlist.idwishlist = wishlist
            producto_wishlist.save()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist_id)

        wishlist = Wishlist.objects.get(id=wishlist_id)
        productos_wishlist = ProductoWishlist.objects.filter(
            idwishlist=wishlist)

        context = {'form': form, 'wishlist': wishlist,
                   'productos_wishlist': productos_wishlist}
        return render(request, self.template_name, context)


class CrearPedidoView(View):
    template_name = "crear_pedido.html"
    form = PedidoForm

    def get(self, request, wishlist_id, subtotal):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        subtotal = subtotal
        form = self.form(initial={'wishlist': wishlist, 'subtotal': subtotal})
        return redirect("index")  # esto está a medias


class WishList(TemplateView, LoginRequiredMixin):
    template_name = "ecommerce/wishlist.html"
    context_object_name = "productos"

    # show wishlist for user if no have wishlist create one for user
    def get(self, request):
        usuario = Cliente.objects.get(idusuario=request.user.id)
        try:
            wishlist = Wishlist.objects.get(idcliente=usuario)
        except Wishlist.DoesNotExist:
            wishlist = Wishlist.objects.create(idcliente=usuario)
        productos = ProductoWishlist.objects.filter(idwishlist=wishlist)
        context = {self.context_object_name: productos}
        return render(request, self.template_name, context)

    # add product to wishlist
    def post(self, request):

        usuario = Cliente.objects.get(idusuario=request.user.id)
        wishlist = Wishlist.objects.get(idcliente=usuario)
        producto = Producto.objects.get(id=request.POST.get("id"))
        cantidad = request.POST.get("cantidad")
        producto_wishlist = ProductoWishlist.objects.create(
            idproducto=producto, idwishlist=wishlist, cantidad=cantidad)
        producto_wishlist.save()
        return redirect("wishlist")

    def delete(self, request):
        usuario = Cliente.objects.get(idusuario=request.user.id)
        wishlist = Wishlist.objects.get(idcliente=usuario)
        producto = Producto.objects.get(id=request.POST.get("id"))
        producto_wishlist = ProductoWishlist.objects.get(
            idproducto=producto, idwishlist=wishlist)
        producto_wishlist.delete()
        return redirect("wishlist")


class PanelUsuario(View, LoginRequiredMixin):
    form = ClienteForm

    def get(self, request):
        usuario = User.objects.get(id=request.user.id)
        form = self.form(initial={'email': usuario.email})
        try:
            cliente = Cliente.objects.get(idusuario=request.user.id)
            form = self.form(instance=cliente)
        except:
            pass
        context = {"form": form}
        return render(request, "panel_usuario.html", context)

    def post(self, request):
        try:
            cliente = Cliente.objects.get(idusuario=request.user.id)
            form = self.form(request.POST, instance=cliente)
        except Cliente.DoesNotExist:
            form = self.form(request.POST)

        if form.is_valid():
            cliente = form.save(commit=False)
            usuario = User.objects.get(id=request.user.id)
            cliente.idusuario = usuario
            cliente.email = usuario.email
            cliente.save()
            return redirect("index")

        context = {"form": form}
        return render(request, "panel_usuario.html", context)

class ProductList(ListView):
    model = Producto
    context_object_name = 'productos'
    ordering = ['nombre']
    template_name = 'product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        #nombre = self.request.GET.get('nombre')
        #precio = self.request.GET.get('valor_unit')
        #descripcion = self.request.GET.get('descripcion')
        #imagen = self.request.GET.get('imagen')

        #if nombre:
        #    queryset = queryset.filter(nombre=nombre)
        #if precio:
        #    queryset = queryset.filter(titulo__icontains=precio)
        return queryset

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = self.object
        nombre = producto.nombre
        valor_unit = producto.valor_unit

        context['valor_unit'] = valor_unit
        return context
