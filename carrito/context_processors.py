from .views import _carrito_sesion
from .models import Carrito
from tienda.models import Producto
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
import locale, decimal


# Contador dinamico de los producto que hay dentro del carrito


# @login_required(login_url="inicio_sesion")
# def mostrar_carrito(request):
#     # Obtener o crear el carrito asociado al usuario actual
#     carrito_user, created = CarritoUser.objects.get_or_create(usuario=request.user)
#     # Obtener todos los ítems de carrito asociados a este usuario
#     items_carrito = Carrito.objects.filter(carritoUser=carrito_user)
#     # Calcular el total del carrito, etc.
#     total = sum(item.producto.precio * item.cantidad for item in items_carrito)
#     return dict(articulo_carrito=items_carrito, total=total)

def mostrar_carrito(request):
    total = 0
    cantidad = 0
    carrito = None
    articulo_carrito = []            

    try:
        if request.user.is_authenticated:
            items_carrito = Carrito.objects.filter(usuario=request.user)            
            print("Carrito autneticado:", items_carrito)
            for articulo in items_carrito:                                
                    total += articulo.producto.precio * articulo.cantidad
                    # articulo_carrito.append({'producto':articulo.producto, 'cantidad':articulo.cantidad})            
        else:
            pass                
    except ObjectDoesNotExist:
        pass
    totalFormato = "{:,.0f}".format(total).replace(",", ".")
    return dict(articulo_carrito=carrito, total=totalFormato)


def contar_productos(request):
    contar = 0
    # if "admin" in request.path:
    #     return {}
    # else:
    #     try:
    #         carrito_sesion = CarritoSesion.objects.filter(
    #             carrito_session=_carrito_sesion(request)
    #         )
    #         if request.user.is_authenticated:
    #             carrito_articulos = Carrito.objects.all().filter(usuario=request.user)
    #         else:
    #             carrito_articulos = Carrito.objects.all().filter(
    #                 carritoSesion=carrito_sesion[:1]
    #             )

    #         for articulo in carrito_articulos:
    #             contar += articulo.activo
    #     except Carrito.DoesNotExist:
    #         contar = 0

    return dict(contar_productos=contar)
