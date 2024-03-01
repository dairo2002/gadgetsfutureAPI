from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroForms
from .models import Cuenta
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

# importaciones email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils import timezone

from carrito.views import _carrito_sesion
from carrito.models import Carrito, CarritoSesion

# API
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_protect

# from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from .serializers import CuentaSerializer

# from .serializers import LoginSerializer


# Instalar: pip install requests permite hacer solicitudes HTTP, como GET,POST..
import requests
import datetime


def registrarse(request):
    if request.method == "POST":
        # Crea una instancia de RegistroForms con los datos del formulario que el usuario ha enviado a través de una solicitud POST.
        formulario = RegistroForms(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data["nombre"]
            apellido = formulario.cleaned_data["apellido"]
            correo_electronico = formulario.cleaned_data["correo_electronico"]
            telefono = formulario.cleaned_data["telefono"]
            password = formulario.cleaned_data["password"]

            # Toma la dirección de correo electrónico y extrae el como nombre de usuario lo que antes símbolo "@", con esto tambien evitamos repetidos
            usuario = correo_electronico.split("@")[0]

            # metodo create_user creado en ManejadorCuenta
            crear_usuario = Cuenta.objects.create_user(
                nombre=nombre,
                apellido=apellido,
                correo_electronico=correo_electronico,
                username=usuario,
                password=password,
            )

            # El campo de telefono es guardado de esta forma porque es un campo obligatorio
            crear_usuario.telefono = telefono
            crear_usuario.save()

            usuarios = auth.authenticate(
                correo_electronico=correo_electronico, password=password
            )

            if usuarios is not None:
                auth.login(request, usuarios)
                messages.success(
                    request,
                    f"Registro exito {usuarios.nombre} {usuarios.apellido}",
                )
            return redirect("index")
    else:
        formulario = RegistroForms()
    return render(request, "cuenta/registrarse.html", {"form": formulario})


def inicio_sesion(request):
    # Verifica si la solicitud al servidor es de tipo POST
    if request.method == "POST":
        # Obtener los datos del formulario
        correo_electronico = request.POST["correo_electronico"]
        password = request.POST["password"]

        #  authenticate: Toma el correo electrónico y la contraseña ingresada, busca un usuario que coincida en la base de datos
        usuarios = auth.authenticate(
            correo_electronico=correo_electronico, password=password
        )

        # Verifica si el usuario no es nulo
        if usuarios is not None:
            # Verificar si hay un carrito existente y asociarlo al usuario
            try:
                carrito_sesion = CarritoSesion.objects.get(
                    carrito_session=_carrito_sesion(request)
                )
                carrito_existe = Carrito.objects.filter(
                    carritoSesion=carrito_sesion
                ).exists()
                if carrito_existe:
                    carrito = Carrito.objects.filter(carritoSesion=carrito_sesion)
                    for articulo in carrito:
                        articulo.usuario = usuarios
                        articulo.save()
            except Exception as e:
                print(f"Error: ", {e})
            # Establece la sesion al usuario
            auth.login(request, usuarios)
            messages.success(
                request, f"Bienvenido {usuarios.nombre} {usuarios.apellido}"
            )
            # Creamos la ruta para que nos redirija a pedidos en caso tal que quiera hacer un pedido
            url = request.META.get("HTTP_REFERER")
            try:
                consulta = requests.utils.urlparse(url).query
                print("Consulta", consulta)
                params = dict(x.split("=") for x in consulta.split("&"))
                print("Parametro: ", params)
                if "next" in params:
                    nextPage = params["next"]
                    return redirect(nextPage)
            except:
                # si no a la pagina de inicio
                return redirect("index")
        else:
            messages.error(request, "Las credenciales son incorrectas")
            return redirect("inicio_sesion")
    return render(request, "cuenta/inicio_sesion.html")


@login_required(login_url="inicio_sesion")
def cerrar_sesion(request):
    auth.logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect("inicio_sesion")


def recuperar_password(request):
    if request.method == "POST":
        correo_electronico = request.POST["correo_electronico"]
        # Hacemos un filtro a la base de datos validando si el correo existe
        if Cuenta.objects.filter(correo_electronico=correo_electronico).exists():
            # Obtener el objeto de usuario asociado al correo electrónico
            usuario = Cuenta.objects.get(correo_electronico__exact=correo_electronico)

            # Obtener el dominio actual
            current_site = get_current_site(request)
            # Configurar el asunto del correo electrónico
            mail_subject = "Recuperar contraseña"
            # Renderizar el mensaje del correo electrónico
            mensaje = render_to_string(
                "cuenta/mensaje_cambiar_pwd.html",
                {
                    "usuario": usuario,
                    "dominio": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(usuario.pk)),
                    "token": default_token_generator.make_token(usuario),
                },
            )

            # Configurar y enviar el correo electrónico
            to_email = correo_electronico
            send_email = EmailMessage(mail_subject, mensaje, to=[to_email])
            send_email.send()

            messages.success(
                request,
                "Se ha enviado un correo electrónico de restablecimiento de contraseña a su dirección de correo electrónico",
            )
            return redirect("inicio_sesion")
        else:
            messages.error(request, "La cuenta no existe!")
            return redirect("recuperar_password")
    return render(request, "cuenta/recuperar_password.html")


# Datos obtenidos para ruta del email
def enlace_cambiar_pwd(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        users = Cuenta._default_manager.get(id=uid)
    except (TypeError, ValueError, OverflowError, Cuenta.DoesNotExist):
        users = None

    if users is not None and default_token_generator.check_token(users, token):
        request.session["uid"] = uid
        messages.success(request, "Por favor restablecer la contraseña")
        return redirect("restablecer_password")
    else:
        messages.error(request, "Este enlace ha caducado!")
        return redirect("inicio_sesion")


def restablecer_password(request):
    if request.method == "POST":
        new_password = request.POST["nueva_password"]
        confirm_password = request.POST["confirmar_password"]

        if new_password == confirm_password:
            uid = request.session.get("uid")
            user = Cuenta.objects.get(id=uid)
            user.set_password(new_password)
            user.save()
            messages.success(
                request,
                "Tu contraseña ha sido guardada, prueba iniciar sesión con tu nueva contraseña",
            )
            return redirect("inicio_sesion")
        else:
            messages.error(request, "Las contraseñas no coniciden")
            return redirect("restablecer_password")
    else:
        return render(request, "cuenta/restablecer_password.html")


# ? APIS

@api_view(["POST"])
def signupAPIView(request):
        serializer = CuentaSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data.get("nombre")
            apellido = serializer.validated_data.get("apellido")
            correo_electronico = serializer.validated_data.get("correo_electronico")
            telefono = serializer.validated_data.get("telefono")
            password = serializer.validated_data.get("password")
            usuario = correo_electronico.split("@")[0]
            # Utiliza tu método personalizado create_user para crear el usuario
            usuario_creado = Cuenta.objects.create_user(
                nombre=nombre,
                apellido=apellido,
                username=usuario,
                correo_electronico=correo_electronico,
                password=password,
            )
            usuario_creado.telefono = telefono
            usuario_creado.save()
            # Genera un token para el usuario registrado
            token, created = Token.objects.get_or_create(user=usuario_creado)
            if created:
                return Response(
                    {
                        "token": token.key,
                        "success": True,
                        "message": f"Bienvenido {usuario_creado.nombre} {usuario_creado.apellido}",
                    },
                    status=status.HTTP_201_CREATED,
                )        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def loginAPIView(request):
    if request.method == "POST":
        correo_electronico = request.data.get("correo_electronico")
        password = request.data.get("password")

        usuario = auth.authenticate(
            correo_electronico=correo_electronico, password=password
        )

        if usuario is not None:
            token, created = Token.objects.get_or_create(user=usuario)

            if created:
                return Response(
                    {
                        "token": token.key,
                        "success": True,
                        "message": f"Bienvenido {usuario.nombre} {usuario.apellido}",
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                # Elmina las sesiones cuando ingresa un navegador, Le creamo un nuevo token cuando el usuario vaya a iniciar sesion
                token.delete()
                token = Token.objects.create(user=usuario)
                return Response(
                    {
                        "token": token.key,
                        "success": True,
                        "message": f"Bienvenido {usuario.nombre} {usuario.apellido}",
                    },
                    status=status.HTTP_200_OK,
                )

        else:
            return Response(
                {"error": False, "message": "Las credenciales son incorrectas"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def logoutAPIView(request):
    try:
        token = request.GET.get("token")
        print(token)
        token = Token.objects.filter(key=token).first()

        if token:
            # user= token.user
            token.user.auth_token.delete()
            return Response(
                {"success": True, "message": "Has cerrado sesión exitosamente."}
            )

        return Response(
            {"error": False, "message": "No se ha encontrado un usuario con este token"}
        )
    except:
        return Response(
            {"error": False, "message": "No se ha encontrado el token en la petición"}
        )


@api_view(['POST'])
def recover_password(request):
    if request.method == "POST":
        correo_electronico = request.data.get("correo_electronico")

        existe_email = Cuenta.objects.filter(correo_electronico=correo_electronico).exists()
        if existe_email:
            usuario = Cuenta.objects.get(correo_electronico__exact=correo_electronico)

            current_site = get_current_site(request)
            # Configurar el asunto del correo electrónico
            mail_subject = "Recuperar contraseña"
            # Renderizar el mensaje del correo electrónico
            mensaje = render_to_string(
                "cuenta/mensaje_cambiar_pwd.html",
                {
                    "usuario": usuario,
                    "dominio": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(usuario.pk)),
                    "token": default_token_generator.make_token(usuario),
                },
            )

            # Configurar y enviar el correo electrónico
            to_email = correo_electronico
            send_email = EmailMessage(mail_subject, mensaje, to=[to_email])
            send_email.send()

            return Response(
                {"message": "Se ha enviado un correo electrónico de restablecimiento de contraseña a su dirección de correo electrónico"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "La cuenta no existe!"},
                status=status.HTTP_404_NOT_FOUND
            )

