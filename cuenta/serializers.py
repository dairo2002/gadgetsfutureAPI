from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Cuenta


class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ["nombre", "apellido", "correo_electronico", "telefono", "password"]


# class LoginSerializer(serializers.ModelSerializer):
#     correo_electronico = serializers.EmailField()
#     password = serializers.CharField()

#     def validate(self, attrs):
#         correo_electronico = attrs.get("correo_electronico")
#         password = attrs.get("password")

#         if correo_electronico and password:
#             user = authenticate(
#                 correo_electronico=correo_electronico, password=password
#             )
#             if not user:
#                 raise serializers.ValidationError(
#                     "Las credenciales son incorrectas", code="authorization"
#                 )
#         else:
#             # Si falta el correo electrónico o la contraseña, levanta un error de validación
#             msg = 'Debe proporcionar tanto el correo electrónico como la contraseña.'
#             raise serializers.ValidationError(msg, code='authorization')
        
#         attrs["user"] = (
#             user  # Almacena el usuario autenticado en los atributos validados
#         )
#         return attrs


# class SinginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cuenta
#         fields = ["nombre", "apellido", "correo_electronico", "telefono", "password"]
