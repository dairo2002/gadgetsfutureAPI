from django.db import models
from tienda.models import Producto
from cuenta.models import Cuenta
import locale, decimal


class CarritoSesion(models.Model):
    carrito_session = models.CharField(max_length=250, blank=True)
    fecha_agregado = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.carrito_session


class Carrito(models.Model):
    carritoSesion = models.ForeignKey(
        CarritoSesion, on_delete=models.CASCADE, null=True
    )
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    activo = models.BooleanField(default=True)
    fecha_agregado = models.DateField(auto_now_add=True)
    # igual a null, lo que indica que no están vinculados a ningún carrito específico. Esto podría ser útil si deseas mantener un historial de los artículos

    def sub_total(self):
        return "{:,.0f}".format(self.operacion()).replace(",",".")

    def operacion(self):
        if self.producto.aplicar_descuento():
            return self.producto.aplicar_descuento() * self.cantidad
        else:
            return self.producto.precio * self.cantidad

    def __unicode__(self):
        return self.producto
