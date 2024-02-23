from django.shortcuts import render
from tienda.models import Producto


def index(request):
    productos = Producto.objects.all().filter(disponible=True)
    return render(request, "index.html", {"producto": productos})
