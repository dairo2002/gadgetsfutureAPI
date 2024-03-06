from rest_framework import serializers
from tienda.models import Producto, Categoria


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"
        # fields = [
        #     "nombre",
        #     "slug",
        #     "descripcion",
        #     "precio",
        #     "stock",
        #     "imagen",
        #     "disponible",
        #     "categoria",
        # ]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria    
        fields = "__all__"
