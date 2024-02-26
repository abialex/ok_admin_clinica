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
from session.models import User
from shared.utils.Global import ERROR_MESSAGE, GET_ROL, SECCUSSFULL_MESSAGE, RolEnum
from rest_framework import status
from shared.utils.baseModel import BaseModelViewSet
from django.db import transaction
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DoctorViewSet(BaseModelViewSet):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = DoctorsResponseSerializer(queryset, many=True)
        custom_data = SECCUSSFULL_MESSAGE(
            tipo=type(self).__name__,
            message="lista de Doctores",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DoctorResponseSerializer(instance)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="Doctor",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        result_serializer = DoctorCreateSerializer(data=request.data)
        if result_serializer.is_valid():
            with transaction.atomic():
                username = "slg_" + result_serializer.data["dni"][:2]
                contrasenia = result_serializer.data["dni"]
                if User.objects.filter(username=username).__len__() > 0:
                    raise IntegrityError("Este username ya existe.")
                user = User.objects.create(
                    username=username,
                    password=make_password(contrasenia),
                )
                doctor = Doctor(
                    nombres=result_serializer.data["nombres"],
                    apellidos=result_serializer.data["apellidos"],
                    dni=result_serializer.data["dni"],
                    celular=result_serializer.data["celular"],
                    fechaNacimiento=result_serializer.data["fechaNacimiento"],
                    usuario_id=user.id,
                )
                doctor.created_by = self.request.user
                doctor.save()

            custom_response_data = SECCUSSFULL_MESSAGE(
                tipo=type(int).__name__,
                message="Doctor creado",
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
        result_serializer = DoctorUpdateSerializer(data=request.data)
        if result_serializer.is_valid():
            with transaction.atomic():
                instance = self.get_object()
                if result_serializer.data.get("ubicaciones") is not None:
                    instance.ubicaciones.set(result_serializer.data["ubicaciones"])
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
                message="Doctor Modificado",
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
        SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="Doctores por Ubicacion",
            url=request.get_full_path(),
            data=serializer.data,
        ),
        status=status.HTTP_200_OK,
    )
