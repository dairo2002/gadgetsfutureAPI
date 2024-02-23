from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from carrito.models import Carrito, CarritoSesion
from carrito.context_processors import _carrito_sesion
from django.contrib import messages

# Q es utilizado para consultas complejas
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Tienda de productos que pertenecen a una categoria
def tienda(request, categoria_slug=None):
    # Verificamos si se ha proporcionado un slug de categoría
    if categoria_slug is not None:
        # Si hay un slug de categoría, obtenemos la categoría correspondiente o retornamos un error 404 si no existe
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        # Filtramos los productos por la categoría seleccionada y que estén disponibles
        productos = Producto.objects.all().filter(categoria=categorias, disponible=True)
        # Contamos la cantidad total de productos en esta categoría
        contar_productos = productos.count()

        # ? Paginacion

        # Configuramos la paginación con la cantidad total de productos
        paginacion = Paginator(productos, len(productos))
        # Obtenemos el número de la página actual desde los parámetros de la solicitud
        pagina_numero = request.GET.get("pagina")
        # Obtenemos la página de productos correspondiente
        pagina_producto = paginacion.get_page(pagina_numero)

    else:
        # Si no se proporciona un slug de categoría, mostramos todos los productos disponibles ordenados por ID
        productos = Producto.objects.all().filter(disponible=True)
        # Contamos la cantidad total de productos disponibles
        contar_productos = productos.count()
        paginacion = Paginator(productos, 3)
        pagina_numero = request.GET.get("pagina")
        pagina_producto = paginacion.get_page(pagina_numero)
    return render(
        request,
        "tienda/tienda.html",
        {"producto": pagina_producto, "contador_producto": contar_productos},
    )


# Tienda un producto unico hacia su detalle
def detalle_producto(request, categoria_slug, producto_slug):
    try:
        # Intenta obtener un único producto filtrando por el slug de la categoría y el slug del producto
        producto_unico = Producto.objects.get(
            categoria__slug=categoria_slug, slug=producto_slug
        )
    except Exception as e:
        raise e

    return render(
        request, "tienda/detalle_producto.html", {"producto_unico": producto_unico}
    )


def filtro_buscar_producto(request):
    palabra_busqueda = None
    contar_productos = 0
    if "txtBusqueda" in request.GET:
        # Si está presente, obtenemos el valor de la palabra clave de la solicitud GET
        txtBusqueda = request.GET["txtBusqueda"]

        # Verificamos si la palabra clave no está vacía
        if txtBusqueda:
            # icontains a un campo de texto en una consulta, la base de datos realizará una búsqueda que ignorará la distinción entre mayúsculas y minúsculas.
            # Q en Django se utiliza para construir expresiones de consulta más complejas, especialmente cuando necesitas combinar condiciones con operadores
            # Operador OR = ('|')
            palabra_busqueda = Producto.objects.filter(
                Q(nombre__icontains=txtBusqueda) | Q(descripcion__icontains=txtBusqueda)
            )

            # Contador de productos encontrados
            contar_productos = palabra_busqueda.count()
            if contar_productos == 0:
                # error_busqueda = (
                #     f"No se encontraron productos que coincidan con la palabra: {txtBusqueda}"
                # )

                return render(
                    request,
                    "tienda/tienda.html",
                    {
                        "error_busqueda": "No se encontraron productos que coincidan con la palabra"
                    },
                )
    # El metodo va a la esta vista tienda.html. por que la vista del navbar.html es incluida en el HTML base, por lo tanto no tiene ruta
    return render(
        request,
        "tienda/tienda.html",
        {
            "producto": palabra_busqueda,
            "contador_producto": contar_productos,
            "txtBuscar": txtBusqueda,
        },
    )


def filtro_rango_precios(request):
    try:
        precio_minimo = float(request.POST.get("min_precio"))
        precio_maximo = float(request.POST.get("max_precio"))
    except ValueError:
        # Mostrar mensaje de error al usuario
        return render(
            request,
            "tienda/tienda.html",
            {"error_precio": "Los valores de precio son inválidos"},
        )

    if precio_minimo is not None and precio_maximo is not None:

        productos = Producto.objects.filter(
            Q(precio__range=[precio_minimo, precio_maximo])
        )
        # Ordenar los producto por el precio menor a mayor
        productos = productos.order_by("precio")
        contar_productos = productos.count()
    else:
        return render(
            request,
            "tienda/tienda.html",
            {"error_precio": "Los valores de precio deben ser números"},
        )
    return render(
        request,
        "tienda/tienda.html",
        {"filtro_precio": productos, "contador_producto": contar_productos},
    )



