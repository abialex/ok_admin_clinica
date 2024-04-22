from enum import Enum
import json
from rest_framework import status
from cita.common import CitaModel
from cita.models import Cita  # , CitaAgil, CitaCompleta, CitaOcupada, CitaTentativa
from cita.serializers import (
    CitaAgilCreateSerializer,
    CitaAgilUpdateSerializer,
    CitaByFechaIdUbicacionIdDoctorSerializer,
    CitaOcupadoCreateSerializer,
    CitaOcupadoUpdateSerializer,
    CitaResponseSerializer,
    CitaSerializer,
    CitasResponseSerializer,
)
from shared.utils.Global import SUCCESS_MESSAGE, STRING
from shared.utils.baseModel import BaseModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from shared.utils.decoradores import validar_data_serializer, validar_serializer


# Create your views here.
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_serializer(serializer=CitaByFechaIdUbicacionIdDoctorSerializer)
def cita_by_fecha_iddoctor_idubicacion(request, data):
    fechaHoraCita = data["fechaHoraCita"]
    doctor_id = data["doctor_id"]
    ubicacion_id = data["ubicacion_id"]

    cita_list = Cita.objects.filter(
        fechaHoraCita__date=fechaHoraCita,
        doctor_id=doctor_id,
        ubicacion_id=ubicacion_id,
    ).order_by("fechaHoraCita")
    cita_ser_list = CitasResponseSerializer(cita_list, many=True)

    return Response(
        SUCCESS_MESSAGE(
            tipo=type(cita_list).__name__,
            message="Citas por Fecha, IdUbicacion y IdDoctor",
            url=request.get_full_path(),
            data=cita_ser_list.data,
        ),
        status=status.HTTP_200_OK,
    )


### CITA VIEWSET ###
class CitaViewSet(BaseModelViewSet):
    queryset = Cita.objects.filter(is_deleted=False)
    # serializer_class = DoctoCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CitasResponseSerializer(queryset, many=True)
        custom_data = SUCCESS_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " list",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CitaResponseSerializer(instance)
        custom_response_data = SUCCESS_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " by-id",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_by = self.request.user
        instance.is_deleted = True
        instance.save()
        custom_response_data = SUCCESS_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " by-ud",
            url="s",
            data=True,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)


### CITA AGIL ###
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_data_serializer(from_dict=Cita.from_dict, serializer=CitaAgilCreateSerializer)
def create_cita_agil(request, data: Cita):
    data.created_by = request.user
    data.save()
    print(status.HTTP_201_CREATED)
    return data.id, status.HTTP_201_CREATED


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_data_serializer(from_dict=Cita.from_dict, serializer=CitaAgilUpdateSerializer)
def update_cita_agil(request, data: Cita):
    cita = Cita.objects.get(id=data.id)
    cita.fechaHoraCita = data.fechaHoraCita
    cita.ubicacion_id = data.ubicacion.id
    cita.estado = data.estado
    cita.datosPaciente = data.datosPaciente
    cita.razon = data.razon
    cita.doctor_id = data.doctor.id
    # base
    cita.updated_by = request.user
    cita.save()
    return data.id, status.HTTP_200_OK


### CITA OCUPADA ###
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_data_serializer(
    from_dict=Cita.from_dict, serializer=CitaOcupadoCreateSerializer
)
def create_cita_ocupado(request, data: Cita):
    data.created_by = request.user
    data.save()
    return data.id, status.HTTP_201_CREATED


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_data_serializer(
    from_dict=Cita.from_dict, serializer=CitaOcupadoUpdateSerializer
)
def update_cita_ocupado(request, data: Cita):
    cita = Cita.objects.get(id=data.id)
    cita.fechaHoraCita = data.fechaHoraCita
    cita.ubicacion_id = data.ubicacion.id
    cita.doctor_id = data.doctor.id
    cita.razonOcupado = data.razonOcupado
    cita.save()
    # base
    cita.updated_by = request.user
    print(status.HTTP_200_OK)
    return data.id, status.HTTP_200_OK
