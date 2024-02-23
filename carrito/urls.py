from django.urls import path
from . import views

urlpatterns = [        
    path("", views.mostrar_carrito, name="mostrar_carrito"),
    path("agregar_carrito/<int:producto_id>/", views.add_carrito, name="add_carrito"),        
    path("eliminar_cantidad/<int:producto_id>/<int:carrito_id>/", views.delete_cantidad_carrito, name="eliminar_cantidad"),
    path("eliminar_producto_carrito/<int:producto_id>/<int:carrito_id>/", views.delete_producto_carrito, name="eliminar_producto_carrito"),
]
