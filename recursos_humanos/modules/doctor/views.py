from datetime import timezone
import datetime
from django.shortcuts import render
from psycopg2 import IntegrityError
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from recursos_humanos.models import Doctor
from recursos_humanos.modules.doctor.serializers import (
    DoctorCreateSerializer,
    DoctorResponseSerializer,
    DoctorUpdateSerializer,
    DoctorsResponseSerializer,
)
from recursos_humanos.views import assignUsername
from session.models import User
from shared.utils.Global import (
    ERROR_MESSAGE,
    GET_ROL,
    SUCCESS_MESSAGE,
    STRING,
    RolEnum,
)
from rest_framework import status
from shared.utils.baseModel import BaseModelViewSet
from django.db import transaction
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from shared.utils.decoradores import validar_serializer


# Create your views here.
class DoctorViewSet(BaseModelViewSet):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = DoctorsResponseSerializer(queryset, many=True)
        custom_data = SUCCESS_MESSAGE(
            tipo=type(self).__name__,
            message="lista de Doctores",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DoctorResponseSerializer(instance)
        custom_response_data = SUCCESS_MESSAGE(
            tipo=type(int).__name__,
            message="Doctor",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    @validar_serializer(serializer=DoctorCreateSerializer)
    def create(self, request, data, *args, **kwargs):
        with transaction.atomic():

            username = assignUsername(dni=data[STRING(Doctor.dni)], prefix="slg_")
            contrasenia = data[STRING(Doctor.dni)]
            if User.objects.filter(username=username).__len__() > 0:
                raise IntegrityError("Este username ya existe.")
            user = User.objects.create(
                username=username,
                password=make_password(contrasenia),
            )
            doctor = Doctor(
                nombres=data[STRING(Doctor.nombres)],
                apellidos=data[STRING(Doctor.apellidos)],
                dni=data[STRING(Doctor.dni)],
                celular=data[STRING(Doctor.celular)],
                fechaNacimiento=data[STRING(Doctor.fechaNacimiento)],
                usuario_id=user.id,
            )
            doctor.created_by = self.request.user
            doctor.save()

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

    @validar_serializer(serializer=DoctorUpdateSerializer)
    def update(self, request, data, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            if data.get(STRING(Doctor.ubicaciones)) is not None:
                instance.ubicaciones.set(data[STRING(Doctor.ubicaciones)])
            instance.nombres = data[STRING(Doctor.nombres)]
            instance.apellidos = data[STRING(Doctor.apellidos)]
            instance.dni = data[STRING(Doctor.dni)]
            instance.celular = data[STRING(Doctor.celular)]
            instance.fechaNacimiento = data[STRING(Doctor.fechaNacimiento)]
            instance.updated_at = datetime.datetime.now()
            instance.updated_by = self.request.user
            instance.save()

        custom_response_data = SUCCESS_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " modificado",
            url=request.get_full_path(),
            data=instance.id,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def doctor_get_by_ubicacion(request):
    rol, personaAsistente = GET_ROL(request.user)
    if rol != RolEnum.ASISTENTE:
        return Response(
            ERROR_MESSAGE(
                tipo=type(int).__name__,
                message="Doctores por Ubicacion",
                url=request.get_full_path(),
                fields_errors="Esta persona no tiene acceso",
            ),
            status=status.HTTP_200_OK,
        )

    doctores = Doctor.objects.filter(
        is_active=True, ubicaciones=personaAsistente.ubicacion.id
    )
    serializer = DoctorsResponseSerializer(doctores, many=True)
    return Response(
        SUCCESS_MESSAGE(
            tipo=type(int).__name__,
            message="Doctores por Ubicacion",
            url=request.get_full_path(),
            data=serializer.data,
        ),
        status=status.HTTP_200_OK,
    )
