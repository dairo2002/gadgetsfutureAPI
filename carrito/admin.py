from django.contrib import admin
from .models import Carrito


class CarritoAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        # "carritoSesion",
        "producto",
        "cantidad",
        "activo",
    )


admin.site.register(Carrito, CarritoAdmin)
