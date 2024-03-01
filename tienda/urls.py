from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.tienda, name="tienda"),
    # Esta ruta muestra los productos que pertenecen a una categoria
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
    # API
    path("api/store/v1/", views.storeAPIView), # NO FUNCIONAL
    path(
        "api/detail_product/v1/<slug:category_slug>/<slug:product_slug>/",
        views.detail_productAPIView,
    ),
    path("api/search_product/v1/", views.searchProductAPIView), 
]
