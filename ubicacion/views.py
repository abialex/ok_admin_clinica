from django.shortcuts import render

from shared.utils.Global import SUCCESS_MESSAGE
from shared.utils.baseModel import BaseModelViewSet
from ubicacion.models import Ubicacion
from ubicacion.serializers import (
    UbicacionResponseSerializer,
    UbicacionsResponseSerializer,
)
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class UbicacionViewSet(BaseModelViewSet):
    queryset = Ubicacion.objects.filter(is_active=True)
    serializer_class = UbicacionsResponseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = UbicacionsResponseSerializer(queryset, many=True)
        custom_data = SUCCESS_MESSAGE(
            tipo=type(self).__name__,
            message="lista de Ubicaciones",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UbicacionResponseSerializer(instance)
        custom_response_data = SUCCESS_MESSAGE(
            tipo=type(int).__name__,
            message="Ubicacion by-id",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    # @validar_serializer(serializer=DoctorCreateSerializer)
    # def create(self, request, data, *args, **kwargs):
    #     with transaction.atomic():

    #         username = assignUsername(dni=data[STRING(Doctor.dni)], prefix="slg_")
    #         password = data[STRING(Doctor.dni)]
    #         if User.objects.filter(username=username).__len__() > 0:
    #             raise IntegrityError("Este username ya existe.")
    #         user = User.objects.create(
    #             username=username,
    #             password=make_password(password),
    #         )
    #         doctor = Doctor(
    #             nombres=data[STRING(Doctor.nombres)],
    #             apellidos=data[STRING(Doctor.apellidos)],
    #             dni=data[STRING(Doctor.dni)],
    #             celular=data[STRING(Doctor.celular)],
    #             fechaNacimiento=data[STRING(Doctor.fechaNacimiento)],
    #             usuario_id=user.id,
    #         )
    #         doctor.created_by = self.request.user
    #         doctor.save()
    #         doctor.ubicaciones.add(*data["ubicaciones_id"])

    #     custom_response_data = SUCCESS_MESSAGE(
    #         tipo=self.queryset.model.__name__,
    #         message=self.queryset.model.__name__ + " creado",
    #         url=request.get_full_path(),
    #         data={
    #             "username": user.username,
    #             "password": password,
    #         },
    #     )
    #     return Response(custom_response_data, status=status.HTTP_201_CREATED)

    # @validar_serializer(serializer=DoctorUpdateSerializer)
    # def update(self, request, data, *args, **kwargs):
    #     with transaction.atomic():
    #         instance = self.get_object()
    #         if data.get("ubicaciones_id") is not None:
    #             instance.ubicaciones.set(data["ubicaciones_id"])
    #         instance.nombres = data[STRING(Doctor.nombres)]
    #         instance.apellidos = data[STRING(Doctor.apellidos)]
    #         instance.dni = data[STRING(Doctor.dni)]
    #         instance.celular = data[STRING(Doctor.celular)]
    #         instance.fechaNacimiento = data[STRING(Doctor.fechaNacimiento)]
    #         instance.updated_at = datetime.datetime.now()
    #         instance.updated_by = self.request.user
    #         instance.save()

    #     custom_response_data = SUCCESS_MESSAGE(
    #         tipo=self.queryset.model.__name__,
    #         message=self.queryset.model.__name__ + " modificado",
    #         url=request.get_full_path(),
    #         data=instance.id,
    #     )
    #     return Response(custom_response_data, status=status.HTTP_200_OK)
