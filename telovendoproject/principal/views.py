import contextlib
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .models import Producto, Pedido, ProductoWishlist, Wishlist, Detalle, Cliente
from .forms import AgregarProductoForm, ClienteForm, EstadoPedidoForm, ProductoForm, ProductoWishlistForm, WishlistForm, PedidoForm, ClienteExternoForm, PedidoExternoForm, PedidoUsuarioForm
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()



class IndexView(View):
    def get(self, request):
        context = {}
        try:
            user = User.objects.get(id=request.user.id)
            context["user"] = user
        except User.DoesNotExist:
            pass
        try:
            cliente = Cliente.objects.get(idusuario=user)
            context["cliente"] = cliente
        except:
            pass
        return render(request, "index.html", context)

 
class PedidosView(View):
    template_name = 'pedidos.html'

    def dispatch(self, request, *args, **kwargs):
        self.usuario = User.objects.get(id=request.user.id)
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            try: 
                self.cliente = Cliente.objects.get(idusuario=self.usuario)
            except Cliente.DoesNotExist:
                alert = "Si desea acceder a la wishlist, primero debe registrar sus datos como cliente"
                messages.error(request, alert)
                return redirect("panel_usuario")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        #Si el usuario es staff, puede ver todos los pedidos
        #en caso contrario, solo renderizara los pedidos del usuario
        if request.user.is_staff:
            pedidos = Pedido.objects.all()
        else:
            pedidos = Pedido.objects.filter(wishlist__idcliente=self.cliente)
            # pedidos = Pedido.objects.filter(wishlist__idcliente=request.user)
        context = {'pedidos': pedidos}
        return render(request, self.template_name, context=context)


@method_decorator(staff_member_required, name='dispatch')
class GestionProdView(View, LoginRequiredMixin):
    template_name = 'gestion_prod.html'

    def get(self, request, *args, **kwargs):
        productos = Producto.objects.all()
        context = {'productos': productos}
        return render(request, self.template_name, context=context)

## Ingresar productos como staff
@method_decorator(staff_member_required, name='dispatch')
class IngresoProductoView(View, LoginRequiredMixin):
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
@method_decorator(staff_member_required, name='dispatch')
class CrearClienteView(View, LoginRequiredMixin):
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
class AgregarProductosWishlistView(View, LoginRequiredMixin):
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
            producto = producto_wishlist.idproducto
            existing_product_wishlist = ProductoWishlist.objects.filter(
                idwishlist=wishlist,
                idproducto=producto
            ).first()

            if existing_product_wishlist:
                existing_product_wishlist.cantidad_deseada += producto_wishlist.cantidad_deseada
                existing_product_wishlist.save()
            else:
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
class CrearPedidoView(View,LoginRequiredMixin):
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
        if subtotal < 50000:
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

## Crear pedido como usuario
class CrearPedidoUsuarioView(View, LoginRequiredMixin):
    template_name = "crear_pedido.html"
    form_class = PedidoUsuarioForm
    reverse_lazy = "pedido_detalle"

    def get(self, request, wishlist_id, cliente_id):
        # get subtotal from agregar_productos_wishlist
        wishlist = Wishlist.objects.get(id=wishlist_id)
        cliente = Cliente.objects.get(id=cliente_id)
        productos_wishlist = ProductoWishlist.objects.filter(
            idwishlist=wishlist)
        subtotal = self.calculate_subtotal(productos_wishlist)
        if subtotal < 50000:
            valordespacho = 5990
        else:
            valordespacho = 0
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
            pedido_detalle = pedido.id
            return redirect(self.reverse_lazy , pedido_detalle)
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

class PedidosList(ListView, LoginRequiredMixin):
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
        if request.POST.get('comprar'):
            return redirect('pedido_usuario', wishlist_id=wishlist_id, cliente_id=wishlist.idcliente.id)

     

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


class ProductDetail(View):
    template_name = 'producto.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.usuario = request.user
        except User.DoesNotExist:
            pass
        try: 
            self.cliente = Cliente.objects.get(idusuario=self.usuario)
        except:
            pass
        try: 
            self.wishlists = Wishlist.objects.filter(idcliente=self.cliente)
        except:
            pass
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        valor_unit = producto.valor_unit
        agregar_producto_form = AgregarProductoForm(cliente=self.cliente)
        context = {
            'producto': producto,
            'valor_unit': valor_unit,
            'agregar_producto_form': agregar_producto_form,
        }
        return render(request, self.template_name, context)


    def post(self, request, pk):
        producto = get_object_or_404(Producto, pk=pk)
        agregar_producto_form = AgregarProductoForm(request.POST, cliente=self.cliente)

        if agregar_producto_form.is_valid():
            cantidad_deseada = agregar_producto_form.cleaned_data['cantidad']
            wishlist_seleccionada = agregar_producto_form.cleaned_data['wishlist']
            producto_wishlist, created = ProductoWishlist.objects.get_or_create(
                idwishlist=wishlist_seleccionada,
                idproducto=producto,
                defaults={'cantidad_deseada': cantidad_deseada}
            )
            if not created:
                producto_wishlist.cantidad_deseada += cantidad_deseada
                producto_wishlist.save()
            alert = "Producto agregado con éxito a la wishlist"
            messages.success(request, alert)
            return redirect('producto', pk=pk)

        context = {
            'producto': producto,
            'valor_unit': producto.valor_unit,
            'agregar_producto_form': agregar_producto_form,
        }
        return render(request, self.template_name, context)


class ContactView(View):
    def get(self, request):
        return render(request, 'contacto.html')
    
## Ejercicio Grupal 5
## Permitirá que los usuarios generales puedan registrar nuevos pedidos asociados a ellos como clientes.


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

# Grupal 6. Detalle del pedido ingresado

class PedidoDetalleView(View):
    template_name = 'detalle_pedido.html'
    def dispatch(self, request, *args, **kwargs):
        self.usuario = User.objects.get(id=request.user.id)
        if request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            try: 
                self.cliente = Cliente.objects.get(idusuario=self.usuario)
            except Cliente.DoesNotExist:
                alert = "Por favor agregué sus datos como cliente"
                messages.error(request, alert)
                return redirect("panel_usuario")
        self.pk = kwargs.get('pk')
        pedido = get_object_or_404(Pedido, pk=self.pk)
        if pedido.wishlist.idcliente == self.cliente:
            pass
        else:
            alert = "No tienes permiso para acceder a ese detalle"
            messages.error(request, alert)
            return redirect("panel_usuario")
        return super().dispatch(request, *args, **kwargs)
   

    def get(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        context = {'pedido': pedido}
        try:
            detalle = Detalle.objects.filter(pedido=pedido)
            print("detalles  ", detalle)
            context["detalle"] = detalle 
        except Detalle.DoesNotExist:
            pass
        if request.user.is_staff:
            form = EstadoPedidoForm(instance=pedido, request=request)
            context["form"] = form
        else:
             pass
        return render(request, 'detalle_pedido.html', context)

    def post(self, request, pk):
        pedido = get_object_or_404(Pedido, pk=pk)
        form = EstadoPedidoForm(request.POST, instance=pedido,request=request)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.estadopedido = form.cleaned_data['estadopedido']
            #get the user from pedido_id and send email
            user = pedido.wishlist.idcliente.idusuario
            send_mail(
                'Estado de pedido',
                'El estado de su pedido ha cambiado a: ' + pedido.estadopedido,
                settings.EMAIL_HOST_USER,
                [user.email],	
                fail_silently=False,
            )
            print("[DEBUG] ", user.email)
            pedido.save()
            return redirect('pedidos')

