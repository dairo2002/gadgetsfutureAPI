from django.shortcuts import render
from tienda.models import Producto

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from tienda.serializers import ProductoSerializer

def index(request):
    productos = Producto.objects.all().filter(disponible=True)
    return render(request, "index.html", {"producto": productos})


@api_view(["GET"])
def listProductAPIView(request):
    queryset = Producto.objects.all().filter(disponible=True)
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)