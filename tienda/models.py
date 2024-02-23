from django.db import models
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from cuenta.models import Cuenta


class Categoria(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descuento = models.DecimalField(
        max_digits=12, decimal_places=0, null=True, blank=True
    )
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    # Ruta de la categoria
    def get_url_categoria(self):
        return reverse("categoria_a_producto", args=[self.slug])

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=3)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to="productos/")
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def get_url_producto(self):
        return reverse("detalle_producto", args=[self.categoria.slug, self.slug])

    def descuento_con_precio(self):
        # Verificar si la categoría tiene un descuento y si las fechas de inicio y fin están definidas
        if (
            self.categoria.descuento
            and self.categoria.fecha_inicio
            and self.categoria.fecha_fin
        ):
            # Verificar si la fecha actual está dentro del rango de fechas de inicio y fin del descuento
            fecha_actual = timezone.now()
            if self.categoria.fecha_inicio <= fecha_actual <= self.categoria.fecha_fin:
                # Convierte el descuento de procentaje a decimal
                descuento_decimal = self.categoria.descuento / 100
                # Calcula el precio con descuento
                precio_descuento = self.precio - (self.precio * descuento_decimal)
                return precio_descuento
            else:
                # Si la fecha actual está fuera del rango de fechas de descuento, limpiar los campos relacionados con el descuento
                self.categoria.descuento = None
                self.categoria.fecha_inicio = None
                self.categoria.fecha_fin = None
                self.categoria.save()
                return self.precio

        return self.precio


class Valoraciones(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=500)
    calificacion = models.FloatField()
    estado = models.BooleanField(default=True)
    creado = models.DateField(default=timezone.now)
    actualizado = models.DateField(default=timezone.now)

    def __str__(self):
        return self.usuario
    



    # TODO Explicacion

    # ? Metodos get_url_categoria y get_url_producto
    # categoria_a_producto es el nombre de la URL, de la categoria
    # con el slug pasamos el id, pero es mostrado en texto
    # def get_url_categoria(self):
    # path("categoria/<slug:categoria_slug>", views.lista_categoria, name="categoria_a_producto"),
    # return reverse('categoria_a_producto', args=[self.slug])
