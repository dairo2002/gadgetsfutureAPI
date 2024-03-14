from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.tienda, name="tienda"),
    # Esta ruta muestra los productos que pertenecen a una categoria
    # name="categoria_a_producto" viene del modelo
    path("categoria/<slug:categoria_slug>/", views.tienda, name="categoria_a_producto"),
    # Ruta de una categoria de un producto, que va hacia el detelle del producto
    path(
        "categoria/<slug:categoria_slug>/<slug:producto_slug>/",
        views.detalle_producto,
        name="detalle_producto",
    ),
    # Ruta busqueda de un producto
    path("buscar/", views.filtro_buscar_producto, name="buscar_producto"),
    path("filtro_precio/", views.filtro_rango_precios, name="filtro_precios"),
    path("valoracion/<int:producto_id>/", views.valoracion, name="valoraciones"),
    # *   API
    # path("api/store/v1/", views.storeAPIView), # Corregir si nos puede servir
    path(
        "categorias/api/category/v1/", views.categoryAPIView
    ),  # Corregir si nos puede servir
    path("categoria/api/store/v1/<int:category_id>/", views.storeAPIView),
    # path("categoria/api/store/v1/<slug:category_slug>/", views.storeAPIView),

    # Filtros
    path("api/search_product/v1/", views.searchProductAPIView),
    path("api/range_price/v1/", views.range_priceAPIView),

    # ? FORMAS DE IR AL DETALLE DE UN PRODUCTO
    path(
        "categoria/api/detail_product/v1/<slug:category_slug>/<slug:product_slug>/",
        views.detail_productAPIView,
    ),
    path(
        "categoria/api/detail_products/v1/<int:category_id>/<int:product_id>/",
        views.detail_productAPIView2,
    ),
    path(
        "categoria/api/detail_products/v1/<int:product_id>/",
        views.detail_productsAPIView,
    ),
]
