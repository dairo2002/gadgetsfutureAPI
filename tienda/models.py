from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from cuenta.models import Cuenta
from django.db.models import Count, Avg

import locale, decimal


class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descuento = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    """
        - reverse: Función de Django para obtener URLs de vistas.
        - categoria_a_producto: Nombre de la vista.
        - args: Lista de argumentos para la vista.
        - self.slug: Atributo del objeto actual (una categoría).
    """

    def get_url_categoria(self):
        return reverse("categoria_a_producto", args=[self.slug])

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to="productos/")
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def get_url_producto(self):
        return reverse("detalle_producto", args=[self.categoria.slug, self.slug])

    # return "{:,.0f}".format(self.precio).replace(",", ".")
    # locale.setlocale(locale.LC_ALL,'es_CO.UTF-8')
    # return locale.currency(self.precio, grouping=True)

    def aplicar_descuento(self):
        if (
            self.categoria.descuento
            and self.categoria.fecha_inicio
            and self.categoria.fecha_fin
        ):

            fecha_actual = timezone.now()
            if self.categoria.fecha_inicio <= fecha_actual <= self.categoria.fecha_fin:
                descuento_decimal = 1 - self.categoria.descuento / 100
                descuento = self.precio * descuento_decimal            
                return descuento
            else:
                # Si la fecha actual está fuera del rango de fechas de descuento, limpiar los campos relacionados con el descuento
                self.categoria.descuento = None
                self.categoria.fecha_inicio = None
                self.categoria.fecha_fin = None
                self.categoria.save()            
                return self.precio
        return self.precio
        
    # ? Otra moneda colombiana   
    # def aplicar_descuento(self):
    #     # Precio formateado a la moneda colombiana
    #     locale.setlocale(locale.LC_ALL, "es_CO")

    #     if (
    #         self.categoria.descuento
    #         and self.categoria.fecha_inicio
    #         and self.categoria.fecha_fin
    #     ):

    #         fecha_actual = timezone.now()
    #         if self.categoria.fecha_inicio <= fecha_actual <= self.categoria.fecha_fin:
    #             descuento_decimal = 1 - decimal.Decimal(self.categoria.descuento / 100)
    #             # descuento_decimal = 1 - (self.categoria.descuento / 100)
    #             descuento = self.precio * descuento_decimal

    #             # precio_formateado = locale.currency(self.precio, grouping=True)
    #             descuento_formateado = locale.currency(descuento, grouping=True)
    #             return descuento_formateado
    #         else:
    #             # Si la fecha actual está fuera del rango de fechas de descuento, limpiar los campos relacionados con el descuento
    #             self.categoria.descuento = None
    #             self.categoria.fecha_inicio = None
    #             self.categoria.fecha_fin = None
    #             self.categoria.save()
    #             precio_formateado = locale.currency(self.precio, grouping=True)
    #             return precio_formateado
    #     else:
    #         precio_formateado = locale.currency(self.precio, grouping=True)
    #         return precio_formateado


    # def aplicar_descuento(self):
    #     # Precio formateado a la moneda colombiana
    #     locale.setlocale(locale.LC_ALL, "es_CO")

    #     if (
    #         self.categoria.descuento
    #         and self.categoria.fecha_inicio
    #         and self.categoria.fecha_fin
    #     ):

    #         fecha_actual = timezone.now()
    #         if self.categoria.fecha_inicio <= fecha_actual and self.categoria.fecha_fin:
    #             descuento_decimal = 1 - (self.categoria.descuento / 100)
    #             descuento = self.precio * descuento_decimal

    #             precio_formateado = locale.currency(self.precio, grouping=True)
    #             descuento_formateado = locale.currency(descuento, grouping=True)

    #             return descuento_formateado, precio_formateado
    #         else:
    #             # Si la fecha actual está fuera del rango de fechas de descuento, limpiar los campos relacionados con el descuento
    #             self.categoria.descuento = None
    #             self.categoria.fecha_inicio = None
    #             self.categoria.fecha_fin = None
    #             self.categoria.save()

    #             precio_formateado = locale.currency(self.precio, grouping=True)
    #             return  descuento_formateado
    #     else:
    #         descuento_formateado = locale.currency(descuento, grouping=True)
    #         return precio_formateado


    # ? Ejemplo hecho por el instructor
    # def descuento_con_precio(self):
    #     # Verificar si la categoría tiene un descuento y si las fechas de inicio y fin están definidas
    #     if (
    #         self.categoria.descuento
    #         and self.categoria.fecha_inicio
    #         and self.categoria.fecha_fin
    #     ):
    #         # Verificar si la fecha actual está dentro del rango de fechas de inicio y fin del descuento
    #         fecha_actual = timezone.now()
    #         if self.categoria.fecha_inicio <= fecha_actual <= self.categoria.fecha_fin:
    #             # Convierte el descuento de procentaje a decimal
    #             descuento_decimal = 1 - (self.categoria.descuento / 100)
    #             # Calcula el precio con descuento
    #             # precio_descuento = self.precio - (self.precio * descuento_decimal)
    #             precio_descuento = self.precio * descuento_decimal
    #             # redondeo a dos decimales
    #             precio_descuento = round(precio_descuento, 2)

    #             precio_descuento_texto = str(precio_descuento)
    #             precio_descuento_arreglo = precio_descuento_texto.split(".")
    #             precio_descuento_texto = precio_descuento_arreglo[0][::-1]
    #             indice = 1
    #             precio_descuento_arreglo[0] = ""
    #             for element in range(0, len(precio_descuento_texto)):
    #                 precio_descuento_arreglo[0] = (
    #                     precio_descuento_arreglo[0] + precio_descuento_texto[element]
    #                 )

    #                 if indice % 3 == 0 and len(precio_descuento_texto) != indice:
    #                     precio_descuento_arreglo[0] = precio_descuento_arreglo[0] + "."

    #                 indice += 1
    #             precio_descuento_texto = precio_descuento_arreglo[0][::-1]
    #             # precio_descuento=Decimal(precio_descuento_texto)
    #             return precio_descuento_texto
    #         else:
    #             # Si la fecha actual está fuera del rango de fechas de descuento, limpiar los campos relacionados con el descuento
    #             self.categoria.descuento = None
    #             self.categoria.fecha_inicio = None
    #             self.categoria.fecha_fin = None
    #             self.categoria.save()
    #             return self.precio

    #     return self.precio





















    def promedioCalificacion(self):
        revisar = Valoraciones.objects.filter(producto=self, estado=True).aggregate(
            promedio=Avg("calificacion")
        )
        avg = 0
        if revisar["promedio"] is not None:
            avg = float(revisar["promedio"])
        return avg

    def contarCalificaciones(self):
        revisar = Valoraciones.objects.filter(producto=self, estado=True).aggregate(
            contar=Count("id")
        )
        contar = 0
        if revisar["contar"] is not None:
            contar = int(revisar["contar"])
        return contar


class Valoraciones(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=500)
    calificacion = models.FloatField()
    estado = models.BooleanField(default=True)
    creado = models.DateField(default=timezone.now)
    actualizado = models.DateField(default=timezone.now)

    def __str__(self):
        return self.usuario.username

    # TODO Explicacion

    # ? Metodos get_url_categoria y get_url_producto
    # categoria_a_producto es el nombre de la URL, de la categoria
    # con el slug pasamos el id, pero es mostrado en texto
    # def get_url_categoria(self):
    # path("categoria/<slug:categoria_slug>", views.lista_categoria, name="categoria_a_producto"),
    # return reverse('categoria_a_producto', args=[self.slug])
