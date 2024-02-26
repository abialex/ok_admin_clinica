import json

from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.sessions.models import Session
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.authtoken.models import Token

from recursos_humanos.serializers import PersonaSerializer

# from core.models import UserRol, UserSede
# from core.serializers import UserRolSerializer, UserSedeSerializer
from session.models import UserTokenFirebase
from session.serializers import *
from shared.utils.Global import DIAS_TOKEN, GET_ROL, SECCUSSFULL_MESSAGE, ERROR_MESSAGE
from shared.utils.baseModel import BaseModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# from Utils import create_response_succes, create_response_error

class UserViewSet(BaseModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserFormSerializer

    def list(self, request, *args, **kwargs):
        # Obtener los datos de la consulta original
        queryset = self.filter_queryset(self.get_queryset())
        # Serializar los datos
        serializer = UsersSerializer(queryset, many=True)
        # Personalizar la respuesta según tus necesidades
        custom_data = SECCUSSFULL_MESSAGE(
            tipo=type(self).__name__,
            message="lista de historias clinicas",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UsersSerializer(instance)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="historia clinica",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        result_serializer = UserFormSerializer(data=request.data)
        if result_serializer.is_valid():

            with transaction.atomic():
                user = User.objects.create(
                    username=result_serializer.data["username"],
                )

                doctor = Doctor(
                    nombres=result_serializer.data["nombres"],
                    apellidos=result_serializer.data["apellidos"],
                    dni=result_serializer.data["dni"],
                    celular=result_serializer.data["celular"],
                    fechaNacimiento=result_serializer.data["fechaNacimiento"],
                    usuario_id=user.id,
                )
                doctor.save()

            custom_response_data = SECCUSSFULL_MESSAGE(
                tipo=type(int).__name__,
                message="historia clinica creada",
                url=request.get_full_path(),
                data=user.id,
            )

            return Response(custom_response_data, status=status.HTTP_201_CREATED)
        else:
            custom_response_data = ERROR_MESSAGE(
                tipo=type(int).__name__,
                message="historia clinica creada",
                url=request.get_full_path(),
                fields_errors=result_serializer.errors,
            )

            return Response(custom_response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="historia clinica modificada",
            url=request.get_full_path(),
            data=response.data["id"],
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí puedes realizar acciones personalizadas al inicializar el ViewSet
        self.initialize_custom_logic()

    def initialize_custom_logic(self):
        # Agrega lógica personalizada que deseas realizar al inicializar el ViewSet
        pass


class AuthTokenLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            diasToken = DIAS_TOKEN - (datetime.now() - token.created).days
            # creando un nuevo token si se vence
            if diasToken < 1:
                token.delete()
                token = Token.objects.create(user=user)
                created = True
                diasToken = 7
            rol, persona = GET_ROL(user)
            response = SECCUSSFULL_MESSAGE(
                tipo=type(user).__name__,
                message="Login",
                url=request.get_full_path(),
                data={
                    "username": user.username,
                    "nombres": persona.nombres + " " + persona.apellidos,
                    "user_id": user.pk,
                    "token": "token " + token.key,
                    "is_new_token": created,
                    "rol": rol.name,
                    "dias_token": diasToken,
                },
            )
            return Response(response)
        else:
            return Response(
                data=ERROR_MESSAGE(
                    tipo="User",
                    message="Credenciales Incorrectos",
                    url=request.get_full_path(),
                    fields_errors={},
                ),
                status=403,
            )


class AuthTokenDelete(ObtainAuthToken):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        token.delete()
        return Response(
            SECCUSSFULL_MESSAGE(
                tipo=type(int).__name__,
                message="Sesión cerrada",
                url=request.get_full_path(),
                data=True,
            )
        )


@api_view(["POST"])
def login_authenticated(request):
    tokenSerializer = TokenSerializer(data=request.data)
    if tokenSerializer.is_valid():
        key = tokenSerializer.data["token"].replace("token ", "")
        token = Token.objects.filter(key=key).first()

        if token:
            daysToken = (datetime.now() - token.created).days
            token_status = "su sesión ha caducado" if daysToken >= DIAS_TOKEN else "ok"
            is_valid = daysToken < DIAS_TOKEN
        else:
            token_status = "Su sesión ha terminado, inicie sesión"
            is_valid = False

        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="token",
            url=request.get_full_path(),
            data={
                "mensaje": token_status,
                "isValid": is_valid,
            },
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)
    else:
        return Response(
            ERROR_MESSAGE(
                tipo=type(int).__name__,
                message="error",
                url=request.get_full_path(),
                fields_errors=tokenSerializer.errors,
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )
