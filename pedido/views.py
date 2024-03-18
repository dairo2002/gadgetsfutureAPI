from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PedidoForm, PagoForm
from .models import Pedido, Pago
from tienda.models import Producto
from carrito.models import Carrito, CarritoSesion
from django.contrib import messages

#
from django.db.models.signals import post_save
from django.dispatch import receiver

# Correo electronico
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from cuenta.models import Cuenta

# API
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import PedidoSerializer

import datetime


@login_required(login_url="inicio_sesion")
def realizar_pedido(request, total=0, cantidad=0):
    usuario_actual = request.user
    carrito = Carrito.objects.filter(usuario=usuario_actual)
    contar_carrito = carrito.count()

    if contar_carrito <= 0:
        return redirect("tienda")

    for articulo in carrito:
        if articulo.producto.aplicar_descuento():
            total += articulo.producto.aplicar_descuento() * articulo.cantidad
            cantidad += articulo.cantidad
        else:
            total += articulo.producto.precio * articulo.cantidad
            cantidad += articulo.cantidad

    if request.method == "POST":
        formulario = PedidoForm(request.POST)
        if formulario.is_valid():
            data = Pedido()
            data.usuario = usuario_actual
            data.nombre = formulario.cleaned_data["nombre"]
            data.apellido = formulario.cleaned_data["apellido"]
            data.telefono = formulario.cleaned_data["telefono"]
            data.correo_electronico = formulario.cleaned_data["correo_electronico"]
            data.direccion = formulario.cleaned_data["direccion"]
            data.direccion_local = formulario.cleaned_data["direccion_local"]
            data.departamento = formulario.cleaned_data["departamento"]
            data.ciudad = formulario.cleaned_data["ciudad"]
            data.codigo_postal = formulario.cleaned_data["codigo_postal"]
            data.total_pedido = total
            data.save()  # Guarda el pedido, para hacer uso del ID en el numero de pedido

            # Numero del pedido: fecha del año, mes, y dia
            year = int(datetime.date.today().strftime("%Y"))
            months = int(datetime.date.today().strftime("%m"))
            day = int(datetime.date.today().strftime("%d"))

            dt = datetime.date(year, months, day)
            fecha_actual = dt.strftime("%Y%m%d")
            # 2024 02 06 1.. ingremento por el id de cada pedido
            num_pedido = fecha_actual + str(data.id)
            data.numero_pedido = num_pedido
            data.save()

            return redirect("pago", id_pedido=data.pk)
    else:
        formulario = PedidoForm()
    return render(request, "client/pedido/realizar_pedido.html", {"form": formulario})


@api_view(["GET", "POST"])
def orderAPIView(request):
    # HACER PRUEBAS MAS ADELANTE
    # total = 0
    # cantidad = 0
    # usuario_actual = request.user
    # carrito = Carrito.objects.filter(usuario=usuario_actual)
    # contar_carrito = carrito.count()

    # if contar_carrito <= 0:
    #     return Response({"message": "No hay artículos en el carrito"}, status=status.HTTP_400_BAD_REQUEST)

    # for articulo in carrito:
    #     if articulo.producto.descuento_con_precio():
    #         total += articulo.producto.descuento_con_precio() * articulo.cantidad
    #         cantidad += articulo.cantidad
    #     else:
    #         total += articulo.producto.precio * articulo.cantidad
    #         cantidad += articulo.cantidad
    if request.method == 'POST':
        serializer = PedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            

def pago(request, id_pedido):
    pedido = get_object_or_404(Pedido, pk=id_pedido)
    if request.method == "POST":
        formulario = PagoForm(request.POST, request.FILES)
        if formulario.is_valid():
            data = Pago()
            data.metodo_pago = formulario.cleaned_data["metodo_pago"]
            data.comprobante = formulario.cleaned_data["comprobante"]
            data.usuario = request.user
            data.cantidad_pagada = pedido.total_pedido
            data.save()

            pedido.pago = data
            pedido.save()

            messages.success(
                request, "Pago exitoso, Se verificara si el comprobante es valido"
            )

            # Filtro eliminar los producto de usuario actual al realizar el pago
            carrito = Carrito.objects.filter(usuario=request.user)
            carrito.delete()
 
            return  redirect("index")
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        formulario = PagoForm()
    return render(request, "client/pedido/pago.html", {"pedido": pedido, "form": formulario})


@receiver(post_save, sender=Pago)
def email_info_pedido(sender, instance, **kwargs):
    if instance.estado_pago == "Aprobado" and instance.estado_envio == "Enviado":
        usuario = instance.usuario

        datos = Pedido.objects.filter(usuario=usuario)
        for pedido in datos:
            pedido.ordenado = True
            pedido.save()

        mail_subject = "¡Su pedido ha sido aprobado!"
        mensaje = render_to_string(
            "client/pedido/email_pago.html",
            {"pedido": pedido},
        )

        to_email = pedido.correo_electronico
        send_email = EmailMessage(mail_subject, mensaje, to=[to_email])
        send_email.send()

        actualizar_stock(instance)


def actualizar_stock(request):
    carrito = Carrito.objects.filter(usuario=request.usuario)
    for articulo in carrito:
        # producto_id acceder al _id 
        producto = Producto.objects.get(pk=articulo.producto_id)
        producto.stock -= articulo.cantidad
        producto.save()
       

# ? API
