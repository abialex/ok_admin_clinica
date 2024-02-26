import datetime
from psycopg2 import IntegrityError

from recursos_humanos.models import Asistente, Doctor, Paciente
from recursos_humanos.modules.paciente.serializers import (
    PacienteCreateSerializer,
    PacienteResponseSerializer,
    PacienteUpdateSerializer,
    PacientesResponseSerializer,
)
from session.models import User
from shared.utils.Global import ERROR_MESSAGE, SECCUSSFULL_MESSAGE
from rest_framework import status
from shared.utils.baseModel import BaseModelViewSet
from django.db import transaction
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class PacienteViewSet(BaseModelViewSet):
    queryset = Paciente.objects.filter(is_active=True)
    # serializer_class = DoctoCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PacientesResponseSerializer(queryset, many=True)
        custom_data = SECCUSSFULL_MESSAGE(
            tipo=type(self).__name__,
            message="lista de Pacientes",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PacienteResponseSerializer(instance)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="Paciente",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        result_serializer = PacienteCreateSerializer(data=request.data)
        if result_serializer.is_valid():
            with transaction.atomic():
                username = result_serializer.data["dni"]
                contrasenia = result_serializer.data["dni"]
                if User.objects.filter(username=username).__len__() > 0:
                    raise IntegrityError("Este username ya existe.")
                user = User.objects.create(
                    username=username,
                    password=make_password(contrasenia),
                )
                asistente = Paciente(
                    nombres=result_serializer.data["nombres"],
                    apellidos=result_serializer.data["apellidos"],
                    dni=result_serializer.data["dni"],
                    celular=result_serializer.data["celular"],
                    fechaNacimiento=result_serializer.data["fechaNacimiento"],
                    usuario_id=user.id,
                )
                asistente.created_by = self.request.user
                asistente.save()

            custom_response_data = SECCUSSFULL_MESSAGE(
                tipo=type(int).__name__,
                message="Paciente creado",
                url=request.get_full_path(),
                data={
                    "username": user.username,
                    "contraseña": contrasenia,
                },
            )
            return Response(custom_response_data, status=status.HTTP_201_CREATED)
        else:
            custom_response_data = ERROR_MESSAGE(
                tipo=type(int).__name__,
                message="error",
                url=request.get_full_path(),
                fields_errors=result_serializer.errors,
            )
            return Response(custom_response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        result_serializer = PacienteUpdateSerializer(data=request.data)
        if result_serializer.is_valid():
            with transaction.atomic():
                instance = self.get_object()
                instance.nombres = result_serializer.data["nombres"]
                instance.apellidos = result_serializer.data["apellidos"]
                instance.dni = result_serializer.data["dni"]
                instance.celular = result_serializer.data["celular"]
                instance.fechaNacimiento = result_serializer.data["fechaNacimiento"]
                instance.updated_at = datetime.datetime.now()
                instance.updated_by = self.request.user
                instance.save()

            custom_response_data = SECCUSSFULL_MESSAGE(
                tipo=type(int).__name__,
                message="Paciente Modificado",
                url=request.get_full_path(),
                data=instance.id,
            )
            return Response(custom_response_data, status=status.HTTP_201_CREATED)
        else:
            custom_response_data = ERROR_MESSAGE(
                tipo=type(int).__name__,
                message="error",
                url=request.get_full_path(),
                fields_errors=result_serializer.errors,
            )
            return Response(custom_response_data, status=status.HTTP_201_CREATED)
