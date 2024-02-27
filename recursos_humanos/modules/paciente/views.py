import datetime
from psycopg2 import IntegrityError

from recursos_humanos.models import Paciente
from recursos_humanos.modules.paciente.serializers import (
    PacienteCreateSerializer,
    PacienteResponseSerializer,
    PacienteUpdateSerializer,
    PacientesResponseSerializer,
)
from session.models import User
from shared.utils.Global import ERROR_MESSAGE, SUCCESS_MESSAGE, STRING
from rest_framework import status
from shared.utils.baseModel import BaseModelViewSet
from django.db import transaction
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from shared.utils.decoradores import validar_serializer


class PacienteViewSet(BaseModelViewSet):
    queryset = Paciente.objects.filter(is_active=True)
    # serializer_class = DoctoCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PacientesResponseSerializer(queryset, many=True)
        custom_data = SUCCESS_MESSAGE(
            tipo=type(self).__name__,
            message="lista de Pacientes",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PacienteResponseSerializer(instance)
        custom_response_data = SUCCESS_MESSAGE(
            tipo=type(int).__name__,
            message="Paciente",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    @validar_serializer(serializer=PacienteCreateSerializer)
    def create(self, request, data, *args, **kwargs):
        with transaction.atomic():
            username = data[STRING(Paciente.dni)]
            contrasenia = data[STRING(Paciente.dni)]
            if User.objects.filter(username=username).__len__() > 0:
                raise IntegrityError("Este username ya existe.")
            user = User.objects.create(
                username=username,
                password=make_password(contrasenia),
            )
            asistente = Paciente(
                nombres=data[STRING(Paciente.nombres)],
                apellidos=data[STRING(Paciente.apellidos)],
                dni=data[STRING(Paciente.dni)],
                celular=data[STRING(Paciente.celular)],
                fechaNacimiento=data[STRING(Paciente.fechaNacimiento)],
                usuario_id=user.id,
            )
            asistente.created_by = self.request.user
            asistente.save()

        custom_response_data = SUCCESS_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " creado",
            url=request.get_full_path(),
            data={
                "username": user.username,
                "contraseña": contrasenia,
            },
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)

    @validar_serializer(serializer=PacienteUpdateSerializer)
    def update(self, request, data, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            instance.nombres = data[STRING(Paciente.nombres)]
            instance.apellidos = data[STRING(Paciente.apellidos)]
            instance.dni = data[STRING(Paciente.dni)]
            instance.celular = data[STRING(Paciente.celular)]
            instance.fechaNacimiento = data[STRING(Paciente.fechaNacimiento)]
            instance.updated_at = datetime.datetime.now()
            instance.updated_by = self.request.user
            instance.save()

        custom_response_data = SUCCESS_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " modificado",
            url=request.get_full_path(),
            data=instance.id,
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)
