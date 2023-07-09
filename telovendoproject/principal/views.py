import contextlib
import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido, ProductoWishlist, Wishlist, Detalle, Cliente
from .forms import ClienteForm, EstadoPedidoForm, ProductoForm, ProductoWishlistForm, WishlistForm, PedidoForm, ClienteExternoForm #DetalleForm
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



class IndexView(View):
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        context = {"user": user}
        try:
            cliente = Cliente.objects.get(idusuario=user)
            context["cliente"] = cliente
        except Cliente.DoesNotExist:
            pass
        return render(request, "index.html", context)

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

## Ingresar productos como staff
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

## Crear cliente y su wishlist como staff
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

## Agrega productos a la wishlist recien creada como staff
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
        form = ProductoWishlistForm(request.POST)
        if request.POST.get('delete'):
            product_id = request.POST.get('delete')
            ProductoWishlist.objects.filter(id=product_id).delete()
            return redirect('agregar_productos_wishlist', wishlist_id=wishlist.id)
        elif request.POST.get('regresar'):
            return redirect('crear_cliente')
        elif request.POST.get('continuar'):
            return redirect('crear_pedido', wishlist_id=wishlist_id, cliente_id=wishlist.idcliente.id)
        elif request.POST.get('guardar_wishlist'):
            return redirect('wishlist_detalle', wishlist_id)

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


## Crear pedido como staff
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


# class WishList(TemplateView, LoginRequiredMixin):
#     template_name = "ecommerce/wishlist.html"

#     def calculate_subtotal(self, productos_wishlist):
#         return sum(
#             producto_wishlist.idproducto.valor_unit
#             * producto_wishlist.cantidad_deseada
#             for producto_wishlist in productos_wishlist
#         )

#     def dispatch(self, request, *args, **kwargs):
#         # Verificar si el usuario es un cliente
#         self.usuario = request.user
#         if not Cliente.objects.filter(idusuario=request.user.id).exists():
#             alert = "Si desea acceder a la wishlist, primero debe registrar sus datos como cliente"
#             messages.error(request, alert)
#             return redirect("panel_usuario")
#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request,  wishlist_id):
#         # Obtener o crear la wishlist del cliente
#         try:
#             wishlist = Wishlist.objects.get(id=wishlist_id)
#         except Wishlist.DoesNotExist:
#             usuario = User.objects.get(id=request.user.id, nombre=request.user.nombre, apellido=request.user.apellido)
#             wishlist = Wishlist.objects.create(idcliente=usuario.id, nombre_wishlist="Wishlist de " + usuario.nombre + " " + usuario.apellido)
#             wishlist.save()
        
#         productos_wishlist = ProductoWishlist.objects.filter(idwishlist=wishlist)
#         subtotal = self.calculate_subtotal(productos_wishlist)
#         form = ProductoWishlistForm()
#         context = {
#             'form': form,
#             'wishlist': wishlist,
#             'productos_wishlist': productos_wishlist,
#             'subtotal': subtotal
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, wishlist_id):
#         wishlist = Wishlist.objects.get(id=wishlist_id)
#         if request.POST.get('delete'):
#             product_id = request.POST.get('delete')
#             ProductoWishlist.objects.filter(id=product_id).delete()
#             return redirect('agregar_productos_wishlist', wishlist_id=wishlist.id)
#         elif request.POST.get('regresar'):
#             return redirect('crear_cliente')
#         elif request.POST.get('continuar'):
#             return redirect('crear_pedido', wishlist_id=wishlist_id, cliente_id=wishlist.idcliente.id)

#         form = ProductoWishlistForm(request.POST)
#         if form.is_valid():
#             producto_wishlist = form.save(commit=False)
#             wishlist = Wishlist.objects.get(id=wishlist_id)
#             producto_wishlist.idwishlist = wishlist
#             producto_wishlist.save()
#             return redirect('agregar_productos_wishlist', wishlist_id=wishlist_id)

#         wishlist = Wishlist.objects.get(id=wishlist_id)
#         productos_wishlist = ProductoWishlist.objects.filter(
#             idwishlist=wishlist)
#         subtotal = self.calculate_subtotal(productos_wishlist)
#         context = {
#             'form': form,
#             'wishlist': wishlist,
#             'productos_wishlist': productos_wishlist,
#             'subtotal': subtotal
#         }
#         return render(request, self.template_name, context)


class ListaWishListView(TemplateView, LoginRequiredMixin):
    template_name = "lista_wishlist.html"
    ## Dispatch se ejecuta primero que cualquier metodo y settea variables desde el comienzo, en este caso el self.usuario a partir del request.user
    def dispatch(self, request, *args, **kwargs):
        self.usuario = User.objects.get(id=request.user.id)
        try: 
            self.cliente = Cliente.objects.get(idusuario=self.usuario)
        except Cliente.DoesNotExist:
            alert = "Si desea acceder a la wishlist, primero debe registrar sus datos como cliente"
            messages.error(request, alert)
            return redirect("panel_usuario")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        wishlist_form = WishlistForm()
        wishlists = Wishlist.objects.filter(idcliente=self.cliente)
        context = {"wishlists": wishlists,
                   "cliente": self.cliente,
                   'wishlist_form': wishlist_form,}
        return render(request, self.template_name, context)
    
    def post(self, request):
        wishlist_form = WishlistForm(request.POST)
        if request.POST.get('crear_wishlist'):
            if wishlist_form.is_valid():
                wishlist = wishlist_form.save(commit=False)
                wishlist.idcliente = self.cliente
                wishlist.save()
                return redirect('user_wishlist')
            return redirect('index')
        
class WishlistDetalleView(TemplateView, LoginRequiredMixin):
    template_name = "wishlist_detalle.html"
    def dispatch(self, request, *args, **kwargs):
        self.usuario = User.objects.get(id=request.user.id)
        try: 
            self.cliente = Cliente.objects.get(idusuario=self.usuario)
        except Cliente.DoesNotExist:
            alert = "Si desea acceder a la wishlist, primero debe registrar sus datos como cliente"
            messages.error(request, alert)
            return redirect("panel_usuario")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        context = {"wishlist": wishlist,
                   "cliente": self.cliente}
        return render(request, self.template_name, context)
    
    def post(self, request, wishlist_id):
        wishlist = Wishlist.objects.get(id=wishlist_id)
        if request.POST.get('delete'):
            product_id = request.POST.get('delete')
            ProductoWishlist.objects.filter(id=product_id).delete()
            return redirect('wishlist_detalle', wishlist_id=wishlist.id)
        if request.POST.get('delete_wishlist'):
            wishlist_id = request.POST.get('delete_wishlist')
            Wishlist.objects.get(id=wishlist_id).delete()
            return redirect('user_wishlist')


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
    
## Ejercicio Grupal 5
## Permitirá que los usuarios generales puedan registrar nuevos pedidos asociados a ellos como clientes.
#
## Vista que permite crear el pedido 
#class CreatePedidoView(View):
#    form_class = PedidoForm
#    template_name = 'pedido_cliente_registrado.html'
#
#    def get(self, request):
#        pedido_form = PedidoForm()
#        detalle_form = DetalleForm()
#        return render(request, 'crear_pedido.html', {'pedido_form': pedido_form, 'detalle_form': detalle_form})
#
#    def post(self, request):
#        pedido_form = PedidoForm(request.POST)
#        detalle_form = DetalleForm(request.POST)
#        
#        if pedido_form.is_valid() and detalle_form.is_valid():
#            pedido = pedido_form.save()
#            detalle = detalle_form.save(commit=False)
#            detalle.pedido = pedido
#            detalle.save()
#            return redirect('detalle_pedido', pedido_id=pedido.id)
#        return render(request, 'crear_pedido.html', {'pedido_form': pedido_form, 'detalle_form': detalle_form})
#
#
##  Vista para agregar productos al carro de compras
#class AgregarProductoView(View):
#    def post(self, request, pedido_id):
#        pedido = Pedido.objects.get(id=pedido_id)
#        form = DetalleForm(request.POST)
#        if form.is_valid():
#            detalle = form.save(commit=False)
#            detalle.pedido = pedido
#            detalle.save()
#            return redirect('detalle_pedido', pedido_id=pedido.id)
#        return render(request, 'detalle_pedido.html', {'pedido': pedido, 'form': form})
#
##  Vista del detalle del carrito de compras
#class CarritoCompraView(View):
#    def get(self, request):
#        # Obtener los productos agregados al carrito del usuario
#        carrito = request.session.get('carrito', {})
#        productos = []
#        total = 0
#
#        # Obtener información de los productos agregados al carrito
#        for producto_id, cantidad in carrito.items():
#            producto = Producto.objects.get(pk=producto_id)
#            subtotal = producto.valor_unit * cantidad
#            total += subtotal
#            productos.append({
#                'producto': producto,
#                'cantidad': cantidad,
#                'subtotal': subtotal
#            })
#
#        context = {
#            'productos': productos,
#            'total': total
#        }
#
#        return render(request, 'carrito_compra.html', context)
#
#    def post(self, request):
#        # Obtener los productos agregados al carrito del usuario
#        carrito = request.session.get('carrito', {})
#        productos = []
#
#        # Crear un nuevo pedido
#        pedido = Pedido()
#        pedido.save()
#
#        # Guardar los detalles de los productos en el pedido
#        for producto_id, cantidad in carrito.items():
#            producto = Producto.objects.get(pk=producto_id)
#            subtotal = producto.valor_unit * cantidad
#
#            detalle = Detalle(
#                pedido=pedido,
#                producto=producto,
#                cantidad=cantidad,
#                valor_unit=producto.valor_unit,
#            )
#            detalle.save()
#
#            productos.append({
#                'producto': producto,
#                'cantidad': cantidad,
#                'subtotal': subtotal
#            })
#
#        # Limpiar el carrito
#        request.session['carrito'] = {}
#
#        context = {
#            'pedido': pedido,
#            'productos': productos
#        }
#
#        return redirect('confirmar_compra')
#
## Vista para confirmar datos y pasar al pago 
#class ConfirmarCompraView(View):
#    def get(self, request):
#        # Obtener el pedido a confirmar
#        pedido_id = request.session.get('pedido_id')
#        pedido = Pedido.objects.get(pk=pedido_id)
#
#        context = {
#            'pedido': pedido
#        }
#
#        return render(request, 'confirmar_compra.html', context)
#
#    def post(self, request):
#        # Obtener el pedido a confirmar
#        pedido_id = request.session.get('pedido_id')
#        pedido = Pedido.objects.get(pk=pedido_id)
#
#        # Obtener la información de despacho ingresada por el cliente
#        direccion_despacho = request.POST.get('direccion_despacho')
#        fecha_despacho = request.POST.get('fecha_despacho')
#
#        # Guardar la información de despacho en el pedido
#        pedido.direccion_despacho = direccion_despacho
#        pedido.fecha_despacho = fecha_despacho
#        pedido.save()
#
#        return redirect('metodo_pago')
#
#
##  Vista para seleccionar forma de pago y generar el pedido
#class MetodoPagoView(View):
#    def get(self, request):
#        # Obtener el pedido a procesar el pago
#        pedido_id = request.session.get('pedido_id')
#        pedido = Pedido.objects.get(pk=pedido_id)
#
#        context = {
#            'pedido': pedido
#        }
#
#        return render(request, 'metodo_pago.html', context)
#
#    def post(self, request):
#        # Obtener el pedido a procesar el pago
#        pedido_id = request.session.get('pedido_id')
#        pedido = Pedido.objects.get(pk=pedido_id)
#
#        # Obtener el método de pago seleccionado por el cliente
#        metodo_pago = request.POST.get('metodo_pago')
#
#        # Guardar el método de pago en el pedido
#        pedido.metodo_pago = metodo_pago
#        pedido.save()
#
#        return redirect('exito_compra')
#