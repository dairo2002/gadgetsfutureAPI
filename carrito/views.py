from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tienda.models import Producto
from .models import  Carrito
from django.urls import resolve
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import locale, decimal
import json


def _carrito_sesion(request):
    # Obtener la clave de sesión actual del usuario
    carrito = request.session.session_key
    # Verificar si el usuario tiene una sesión activa (si carrito es nulo o vacío)
    if not carrito:
        # Si no hay una sesión activa, crear una nueva sesión y obtener su clave
        carrito = request.session.create()
        # Devolver la clave de sesión (puede ser la existente o la recién creada)
    return carrito



def add(request, producto_id):
    if request.method == "POST":
        cantidad_str = request.POST.get("txtCantidad")
        if cantidad_str is not None and cantidad_str.isdigit():
            cantidad = int(cantidad_str)
            if cantidad > 0:
                producto = get_object_or_404(Producto, pk=producto_id)
                if producto.stock >= cantidad:  
                    if request.user.is_authenticated:                  
                        # itemCarrito = Carrito()
                        # carrito = CarritoUser()
                    
                        item, created = Carrito.objects.get_or_create(producto=producto, cantidad=cantidad)  
                        if not created:
                            item.cantidad += cantidad
                        else:
                            item.cantidad = cantidad
                        item.save()
                        print("producto: ",producto )
                        print("cantidad: ",cantidad )
                        return redirect('mostrar_carrito')
                    else:                         
                        item, created = Carrito.objects.get_or_create(producto=producto, cantidad=cantidad)  
                        if not created:
                            item.cantidad += cantidad
                        else:
                            item.cantidad = cantidad
                        item.save()
                        print("producto: ",producto )
                        print("cantidad: ",cantidad )
                        return redirect('inicio_sesion')
                else:
                    messages.error(request, "La cantidad solicitada excede el stock disponible")    
            else:
                messages.error(request, "La cantidad debe ser mayor que 0")
        else:
            messages.error(request, "La cantidad no es un número válido")
    return redirect("mostrar_carrito")            


# def add_user_authenticated(usuario, producto, cantidad):
#     if Carrito.object.filter(usuario=usuario, producto=producto, cantidad=cantidad):
#         carrito = Carrito.objects.get(usuario=usuario, producto=producto)
#         carrito.cantidad += cantidad
#         carrito.save()
#     else:
#         carrito = Carrito(usuario=usuario, producto=producto, cantidad=cantidad)
#         carrito.save()

# def add_user_temporal(request, producto_id, cantidad):    
#     carrito_temporal = request.session.get('carrito_temporal', [])
#     producto_info = {'producto': producto, 'cantidad': cantidad}
#     carrito_temporal.append(producto_info)
#     request.session['carrito_temporal'] = carrito_temporal
#     request.session.modified = True

@login_required(login_url="inicio_sesion")
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
            carrito = Carrito.objects.get(
                producto=producto, id=carrito_id
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
        carrito = Carrito.objects.get(
            producto=producto, id=carrito_id
        )
    carrito.delete()
    return redirect("mostrar_carrito")
