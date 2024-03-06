from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, Valoraciones
from pedido.models import Pedido
from carrito.models import Carrito, CarritoSesion
from carrito.views import _carrito_sesion
from django.contrib import messages
from .forms import ValoracionesForm

# Q es utilizado para consultas complejas
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# API
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductoSerializer, CategoriaSerializer


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
        paginacion = Paginator(productos, 4)
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

        # TODO Creamos esta linea de codigo para saber si el producto ya esta agregado al carrito,
        # TODO Si esta agregado en vista producto detalle, el boton de agregar al carrito va a cambiar a ir a carrito
        carrito = Carrito.objects.filter(
            carritoSesion__carrito_session=_carrito_sesion(request),
            producto=producto_unico,
        ).exists()
    except Exception as e:
        raise e

    # filtramos si el usuario ya a comprado el producto
    if request.user.is_authenticated:
        try:
            pedido = Pedido.objects.filter(usuario=request.user, ordenado=True).exists()
        except Pedido.DoesNotExist:
            pedido = None
    else:
        pedido = None

    reviews = Valoraciones.objects.filter(producto_id=producto_unico.id, estado=True)

    return render(
        request,
        "tienda/detalle_producto.html",
        {
            "producto_unico": producto_unico,
            "review": reviews,
            "pedido": pedido,
            "carrito": carrito,
        },
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


# ? Corregir que el filtro pueda buscar con decimales, Tambien la API
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


@api_view(["POST"])
def range_priceAPIView(request):
    try:
        precio_minimo = float(request.GET.get("min_precio"))
        precio_maximo = float(request.GET.get("max_precio"))
    except ValueError:
        return Response(
            {"error": "Los valores de precio son inválidos"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if precio_minimo is not None and precio_maximo is not None:
        productos = Producto.objects.filter(
            Q(precio__range=[precio_minimo, precio_maximo])
        ).order_by("precio")

        # Ordenar los productos por precio de menor a mayor
        # productos = productos.order_by("precio")
        # Contador de productos
        contar_productos = productos.count()

    else:
        return Response(
            {"error": "Los valores de precio deben ser número"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# ? Terminar
def valoracion(request, producto_id):
    # almacena la ruta anterior, para ser redirijidad
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            # ? __id una forma de acceder al id, del ese modelo
            valoracion = Valoraciones.objects.get(
                usuario__id=request.user.id, producto__id=producto_id
            )
            # Trear el formulario
            # pasamos una instanca si el usuario ya tiene una reseña, entonces para que pueda actualizar esa reseña
            form = ValoracionesForm(request.POST, instance=valoracion)
            form.save()
            messages.success(request, "Tu reseña ha sido actualizada")
            return redirect(url)
        except Valoraciones.DoesNotExist:
            form = ValoracionesForm(request.POST)
            if form.is_valid():
                data = Valoraciones()
                data.calificacion = form.cleaned_data["calificacion"]
                data.comentario = form.cleaned_data["comentario"]
                data.producto_id = producto_id
                data.usuario_id = request.user.id
                data.save()
                messages.success(request, "Tu reseña ha sido enviada")
                return redirect(url)

# ? APIS
@api_view(["GET"])
def categoryAPIView(request):
    queryset = Categoria.objects.all()
    serializer = CategoriaSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#  Me trae los productos de una categoría
@api_view(["GET"])
def storeAPIView(request, category_slug=None):
    if category_slug is not None:
        categorias = get_object_or_404(Categoria, slug=category_slug)
        productos = Producto.objects.all().filter(categoria=categorias, disponible=True)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "No se encontro el producto con la categoria"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# Detalle de un unico producto
@api_view(["GET"])
def detail_productAPIView(request, category_slug, product_slug):
    try:
        # Intenta obtener un único producto filtrando por el slug de la categoría y el slug del producto
        categoria = get_object_or_404(Categoria, slug=category_slug)
        producto = get_object_or_404(Producto, categoria=categoria, slug=product_slug)

        serializer = ProductoSerializer(producto)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Producto.DoesNotExist:
        return Response(
            {"error": "Lista de productos no encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )

# Buscador de un producto
@api_view(["POST"])
def searchProductAPIView(request):
    palabra_clave = None
    contar_productos = 0

    palabra_clave = request.GET.get("txtBusqueda")

    if palabra_clave:
        productos_encontrados = Producto.objects.filter(
            Q(nombre__icontains=palabra_clave) | Q(descripcion__icontains=palabra_clave)
        )

        contar_productos = productos_encontrados.count()
        if contar_productos == 0:
            return Response(
                {"error": "No se encontraron productos que coincidan con la búsqueda"},
                status=status.HTTP_404_NOT_FOUND,
            )

    # Serializar todos los productos encontrados, en caso de que no funcion crear un serializer para search product
    serializer = ProductoSerializer(productos_encontrados, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


