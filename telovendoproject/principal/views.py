import contextlib
import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido, ProductoWishlist, Wishlist, Detalle, Cliente
from .forms import ClienteForm, EstadoPedidoForm, ProductoForm, ProductoWishlistForm, WishlistForm, PedidoForm, ClienteExternoForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages

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
        form = ClienteExternoForm()
        wishlist_form = WishlistForm()
        clientes = Cliente.objects.all()
        context = {'form': form,
                'wishlist_form': wishlist_form,
                'clientes': clientes}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ClienteExternoForm(request.POST)
        wishlist_form = WishlistForm(request.POST)

        if request.POST.get('cliente_existente'):
            cliente = Cliente.objects.get(
                id=request.POST.get('cliente_existente'))
        elif form.is_valid() and wishlist_form.is_valid():
            cliente = form.save()
        wishlist = wishlist_form.save(commit=False)
        wishlist.idcliente = cliente
        wishlist.save()
        return redirect('agregar_productos_wishlist', wishlist_id=wishlist.id)


class AgregarProductosWishlistView(View):
    template_name = 'agregar_productos_wishlist.html'

    def calculate_subtotal(self, productos_wishlist):
        return sum(
            producto_wishlist.idproducto.valor_unit
            * producto_wishlist.cantidad_deseada
            for producto_wishlist in productos_wishlist
        )

    def get(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        productos_wishlist = ProductoWishlist.objects.filter(
            idwishlist=wishlist)
        subtotal = self.calculate_subtotal(productos_wishlist)
        form = ProductoWishlistForm()
        context = {
            'form': form,
            'wishlist': wishlist,
            'productos_wishlist': productos_wishlist,
            'subtotal': subtotal
        }
        return render(request, self.template_name, context)

    def post(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        if request.POST.get('delete'):
            product_id = request.POST.get('delete')
            ProductoWishlist.objects.filter(id=product_id).delete()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist.id)
        elif request.POST.get('regresar'):
            return redirect('crear_cliente')
        elif request.POST.get('continuar'):
            return redirect('crear_pedido', wishlist_id=wishlist_id, cliente_id=wishlist.idcliente.id)

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
        subtotal = self.calculate_subtotal(productos_wishlist)
        context = {
            'form': form,
            'wishlist': wishlist,
            'productos_wishlist': productos_wishlist,
            'subtotal': subtotal
        }
        return render(request, self.template_name, context)



class CrearPedidoView(View):
    template_name = "crear_pedido.html"
    form_class = PedidoForm
    reverse_lazy = "pedidos"

    def get(self, request, wishlist_id, cliente_id):
        # get subtotal from agregar_productos_wishlist
        wishlist = Wishlist.objects.get(id=wishlist_id)
        cliente = Cliente.objects.get(id=cliente_id)
        productos_wishlist = ProductoWishlist.objects.filter(
            idwishlist=wishlist)
        subtotal = self.calculate_subtotal(productos_wishlist)
        valordespacho = 0
        if valordespacho < 50000:
            valordespacho = 5990
        valortotal = valordespacho + subtotal
        form = self.form_class(
            initial={'wishlist': wishlist, 
                     'subtotal': subtotal,
                    'valordespacho': valordespacho,
                    'valortotal': valortotal})
        context = {
            'form': form,
            'wishlist': wishlist,
            'subtotal': subtotal,
            'cliente': cliente
        }
        return render(request, self.template_name, context)

    def post(self, request, wishlist_id, cliente_id):
        form = self.form_class(request.POST)
        wishlist = Wishlist.objects.get(id=wishlist_id)
        productos_wishlist = wishlist.productos.through.objects.filter(idwishlist=wishlist)
        if form.is_valid():
            pedido = form.save()
            pedido.wishlist_id = wishlist
            pedido.save()
            self.crear_detalle(wishlist, pedido)
            return redirect(self.reverse_lazy)
        else:
            print(form.errors)

        wishlist = Wishlist.objects.get(id=wishlist_id)
        cliente = Cliente.objects.get(id=cliente_id)
        productos_wishlist = ProductoWishlist.objects.filter(
            idwishlist=wishlist)
        subtotal = self.calculate_subtotal(productos_wishlist)
        context = {
            'form': form,
            'wishlist': wishlist,
            'subtotal': subtotal,
            'cliente': cliente
        }
        return render(request, self.template_name, context)
        
    def calculate_subtotal(self, productos_wishlist):
        return sum(
            producto_wishlist.idproducto.valor_unit
            * producto_wishlist.cantidad_deseada
            for producto_wishlist in productos_wishlist
        )

    def crear_detalle(self, wishlist, pedido):
        productos_wishlist = wishlist.productos.through.objects.filter(idwishlist=wishlist)
        for producto_wishlist in productos_wishlist:
            producto = producto_wishlist.idproducto
            cantidad_deseada = producto_wishlist.cantidad_deseada
            detalle = Detalle()
            detalle.pedido = pedido 
            detalle.productos = producto 
            detalle.cantidad = cantidad_deseada 
            detalle.valor_unit = producto.valor_unit 
            detalle.save()


class PedidosList(ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedidos.html'
    
    def get_queryset(self):
        return super().get_queryset()




class WishList(TemplateView, LoginRequiredMixin):
    template_name = "ecommerce/wishlist.html"

    def calculate_subtotal(self, productos_wishlist):
        return sum(
            producto_wishlist.idproducto.valor_unit
            * producto_wishlist.cantidad_deseada
            for producto_wishlist in productos_wishlist
        )

    def get(self, request,  wishlist_id):
        # Verificar si el usuario es un cliente
        if not Cliente.objects.filter(idusuario=request.user.id).exists():
            alert = "Si desea acceder a la wishlist, primero debe registrarse como cliente"
            messages.error(request, alert)
            return redirect("panel_usuario")
        
        # Obtener o crear la wishlist del cliente
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id)
        except Wishlist.DoesNotExist:
            usuario = User.objects.get(id=request.user.id, nombre=request.user.nombre, apellido=request.user.apellido)
            wishlist = Wishlist.objects.create(idcliente=usuario.id, nombre_wishlist="Wishlist de " + usuario.nombre + " " + usuario.apellido)
            wishlist.save()
        
        productos_wishlist = ProductoWishlist.objects.filter(idwishlist=wishlist)
        subtotal = self.calculate_subtotal(productos_wishlist)
        form = ProductoWishlistForm()
        context = {
            'form': form,
            'wishlist': wishlist,
            'productos_wishlist': productos_wishlist,
            'subtotal': subtotal
        }
        return render(request, self.template_name, context)

    def post(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        if request.POST.get('delete'):
            product_id = request.POST.get('delete')
            ProductoWishlist.objects.filter(id=product_id).delete()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist.id)
        elif request.POST.get('regresar'):
            return redirect('crear_cliente')
        elif request.POST.get('continuar'):
            return redirect('crear_pedido', wishlist_id=wishlist_id, cliente_id=wishlist.idcliente.id)

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
        subtotal = self.calculate_subtotal(productos_wishlist)
        context = {
            'form': form,
            'wishlist': wishlist,
            'productos_wishlist': productos_wishlist,
            'subtotal': subtotal
        }
        return render(request, self.template_name, context)



class PanelUsuario(View, LoginRequiredMixin):
    form = ClienteForm

    def get(self, request):
        usuario = User.objects.get(id=request.user.id)
        form = self.form(initial={'email': usuario.email})
        with contextlib.suppress(Exception):
            cliente = Cliente.objects.get(idusuario=request.user.id)
            form = self.form(instance=cliente)
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
        return super().get_queryset()


class ProductDetail(DetailView):
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


class ContactView(View):
    def get(self, request):
        return render(request, 'contacto.html')