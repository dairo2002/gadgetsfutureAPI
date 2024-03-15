from django.shortcuts import render, redirect, get_object_or_404
from tienda.models import Producto
from .models import CarritoSesion, Carrito
from django.urls import resolve
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
import locale, decimal


def _carrito_sesion(request):
    # Obtener la clave de sesión actual del usuario
    carrito = request.session.session_key
    # Verificar si el usuario tiene una sesión activa (si carrito es nulo o vacío)
    if not carrito:
        # Si no hay una sesión activa, crear una nueva sesión y obtener su clave
        carrito = request.session.create()
        # Devolver la clave de sesión (puede ser la existente o la recién creada)
    return carrito


# ! Corregir
def add_carrito(request, producto_id):
    current_user = request.user
    producto = Producto.objects.get(id=producto_id)

    if current_user.is_authenticated:
        carrito_existente = Carrito.objects.filter(
            producto=producto, usuario=current_user
        ).exists()
        if carrito_existente:
            carrito = Carrito.objects.get(producto=producto, usuario=current_user)
            carrito.cantidad += 1
            carrito.save()
        else:
            carrito = Carrito.objects.create(
                producto=producto, cantidad=1, usuario=current_user
            )

    else:
        try:
            session = CarritoSesion.objects.get(
                carrito_session=_carrito_sesion(request)
            )
        except CarritoSesion.DoesNotExist:
            session = CarritoSesion.objects.create(
                carrito_session=_carrito_sesion(request)
            )
        session.save()

        carrito_existente = Carrito.objects.filter(
            producto=producto, carritoSesion=session
        ).exists()

        if carrito_existente:
            carrito = Carrito.objects.get(producto=producto, carritoSesion=session)
            carrito.cantidad += 1
            carrito.save()
        else:
            carrito = Carrito.objects.create(
                producto=producto, cantidad=1, carritoSesion=session
            )

    return redirect("mostrar_carrito")


# Vista que va hacia el carrito


def mostrar_carrito(request):
    # Renderizamos la pagina, para dar una ruta
    # la Funcionalidad esta en el context_proccesor
    # Al esta en el context_proccesor nos permite visualizar los productos de carrito en varias vistas  
    return render(request, "client/tienda/carrito.html")


# Eliminar un producto por la cantidad
def delete_cantidad_carrito(request, producto_id, carrito_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    try:
        if request.user.is_authenticated:
            carrito = Carrito.objects.get(
                producto=producto, usuario=request.user, id=carrito_id
            )
        else:
            carrito_sesion = CarritoSesion.objects.get(
                carrito_session=_carrito_sesion(request)
            )
            carrito = Carrito.objects.get(
                producto=producto, carritoSesion=carrito_sesion, id=carrito_id
            )
        #  Actualización de la cantidad del carrito
        if carrito.cantidad > 1:
            # Si la cantidad es mayor que 1, se disminuye en 1 y se guarda
            carrito.cantidad -= 1
            carrito.save()
        else:
            # Eliminación del producto del carrito si la cantidad es 1 o menos
            carrito.delete()
    except:
        pass
    return redirect("mostrar_carrito")


def delete_producto_carrito(request, producto_id, carrito_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.user.is_authenticated:
        carrito = Carrito.objects.get(
            producto=producto, usuario=request.user, id=carrito_id
        )
    else:
        carrito_sesion = CarritoSesion.objects.get(
            carrito_session=_carrito_sesion(request)
        )
        carrito = Carrito.objects.get(
            producto=producto, carritoSesion=carrito_sesion, id=carrito_id
        )
    carrito.delete()
    return redirect("mostrar_carrito")
