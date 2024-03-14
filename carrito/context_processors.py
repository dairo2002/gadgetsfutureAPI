from .views import _carrito_sesion
from .models import Carrito, CarritoSesion
from tienda.models import Producto
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
import locale, decimal



# Muestra los productos que hay en el carrito de compras, utilizado en carrito.html y navbar.html
def mostrar_carrito(request, total=0, cantidad=0, carrito=None):
    try:
        if request.user.is_authenticated:
            carrito = Carrito.objects.filter(usuario=request.user, activo=True)
        else:
            carrito_sesion = CarritoSesion.objects.get(
                carrito_session=_carrito_sesion(request)
            )
            carrito = Carrito.objects.filter(carritoSesion=carrito_sesion, activo=True)
        for articulo in carrito:
            descuento_aplicado = articulo.producto.aplicar_descuento()
            if isinstance(descuento_aplicado, (int, float)):                                
                total += descuento_aplicado + descuento_aplicado 
                cantidad += articulo.cantidad
            else:
                total = descuento_aplicado + descuento_aplicado * articulo.cantidad
                cantidad += articulo.cantidad
    except ObjectDoesNotExist:
        pass

    return dict(total=total, articulo_carrito=carrito)













# def mostrar_carrito(request, total=0, cantidad=0, carrito=None):
#     try:
#         if request.user.is_authenticated:
#             carrito = Carrito.objects.filter(usuario=request.user, activo=True)
#         else:
#             carrito_sesion = CarritoSesion.objects.get(
#                 carrito_session=_carrito_sesion(request)
#             )
#             carrito = Carrito.objects.filter(carritoSesion=carrito_sesion, activo=True)
#         for articulo in carrito:
#             if articulo.producto.aplicar_descuento():
#                 descuento_aplicado = articulo.producto.aplicar_descuento()
#                 total += descuento_aplicado * articulo.cantidad
#                 cantidad += articulo.cantidad
#             else:
#                 total += articulo.producto.aplicar_descuento() * articulo.cantidad
#                 cantidad += articulo.cantidad
#     except ObjectDoesNotExist:
#         pass

#     return dict(total=total, articulo_carrito=carrito)


# Contador dinamico de los producto que hay dentro del carrito
def contar_productos(request):
    contar = 0
    if "admin" in request.path:
        return {}
    else:
        try:
            carrito_sesion = CarritoSesion.objects.filter(
                carrito_session=_carrito_sesion(request)
            )
            if request.user.is_authenticated:
                carrito_articulos = Carrito.objects.all().filter(usuario=request.user)
            else:
                carrito_articulos = Carrito.objects.all().filter(
                    carritoSesion=carrito_sesion[:1]
                )

            for articulo in carrito_articulos:
                contar += articulo.activo
        except Carrito.DoesNotExist:
            contar = 0

    return dict(contar_productos=contar)
