from django.urls import path, include
from . import views

urlpatterns = [
    path("registrarse/", views.registrarse, name="registrarse"),
    path("inicio_sesion/", views.inicio_sesion, name="inicio_sesion"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("recuperar_password/", views.recuperar_password, name="recuperar_password"),
    path(
        "cambiar_password/<uidb64>/<token>/",
        views.enlace_cambiar_pwd,
        name="enlace_cambiar_pwd",
    ),
    path(
        "restablecer_password/", views.restablecer_password, name="restablecer_password"
    ),

    # API
    path("api/login/v1/", views.loginAPIView),
    # path("api/login/v1/", views.loginAPIView.as_view()),
]
