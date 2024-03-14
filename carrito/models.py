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
        if self.producto.aplicar_descuento():
            return self.producto.aplicar_descuento() * self.cantidad    
        else:
            return self.producto.precio * self.cantidad        


    # ? Otra forma de moneda, no funciona  
    # def sub_total(self):
    #     locale.setlocale(locale.LC_ALL, "es_CO")
        
    #     if self.producto.aplicar_descuento():          
    #         descuento = self.producto.aplicar_descuento()  * self.cantidad         
    #         return descuento
    #     else:
    #         precio = self.producto.precio * self.cantidad
    #         precio_formato = locale.currency(precio, grouping=True)
    #         return precio_formato
  

    def __unicode__(self):
        return self.producto
