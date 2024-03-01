from rest_framework import serializers
from tienda.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "slug",
            "descripcion",
            "precio",
            "stock",
            "imagen",
            "disponible",
            "categoria",
        ]
