import json
from .views import _carrito_sesion
from .models import Carrito, CarritoSesion
from tienda.models import Producto
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
import locale, decimal


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


def mostrar_carrito(request):
    total = 0
    cantidad = 0
    carrito = None
    articulo_carrito = []            

    try:
        if request.user.is_authenticated:
            carrito = Carrito.objects.filter(usuario=request.user, activo=True)
            print("Carrito autneticado:", carrito)
            for articulo in carrito:                                
                    total += articulo.producto.precio * articulo.cantidad
                    articulo_carrito.append({'producto':articulo.producto, 'cantidad':articulo.cantidad})            
        else:
            carrito_temporal = request.session.get('carrito_temporal', {})   
            print("carrito temporal", carrito_temporal)         
            for prod_id, cantidad in carrito_temporal.items():                
                producto = get_object_or_404(Producto, pk=prod_id)
                total +=producto.precio * cantidad
                articulo_carrito.append({'producto':producto, 'cantidad':cantidad})                                
    except ObjectDoesNotExist:
        pass

    totalFormato = "{:,.0f}".format(total).replace(",", ".")
    return dict(total=totalFormato, articulo_carrito=carrito)

# def mostrar_carrito(request):
#     try:
#         total = 0
#         cantidad = 0
#         carrito = None

#         if request.user.is_authenticated:
#             carrito = Carrito.objects.filter(usuario=request.user, activo=True)
#         else:
#             carrito_sesion = CarritoSesion.objects.get(
#                 carrito_session=_carrito_sesion(request)
#             )

#             carrito = Carrito.objects.filter(carritoSesion=carrito_sesion, activo=True)
#             print("carrito: ", carrito)
#         for articulo in carrito:
#             if articulo.producto.aplicar_descuento():
#                 descuento = articulo.producto.aplicar_descuento()
#                 total += descuento * articulo.cantidad
#                 cantidad += articulo.cantidad
#             else:
#                 total += articulo.producto.precioFormatiado() * articulo.cantidad
#                 cantidad += articulo.cantidad
#     except ObjectDoesNotExist:
#         pass

#     totalFormato = "{:,.0f}".format(total).replace(",", ".")
#     return dict(total=totalFormato, articulo_carrito=carrito)
