import datetime
from enum import Enum
import json
from rest_framework import status
from cita.choices import EstadoCita
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
from shared.utils.Global import ERROR_MESSAGE, SUCCESS_MESSAGE, STRING
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
from django.db.models import Q


# Create your views here.
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_serializer(serializer=CitaByFechaIdUbicacionIdDoctorSerializer)
def cita_by_fecha_iddoctor_idubicacion(request, data):
    fechaHoraCita = data["fechaHoraCita"]
    doctor_id = data["doctor_id"]
    ubicaciones_id = data["ubicaciones_id"]

    cita_list = (
        Cita.objects.filter(
            fechaHoraCita__date=fechaHoraCita,
            doctor_id=doctor_id,
        )
        .filter(Q(ubicacion_id__in=ubicaciones_id) | Q(ubicacion=None))
        .exclude(is_deleted=True)
        .order_by("fechaHoraCita")
    )
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
            message=self.queryset.model.__name__ + "delete by-id",
            url=request.get_full_path(),
            data=True,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)


### CITA AGIL ###
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_data_serializer(from_dict=Cita.from_dict, serializer=CitaAgilCreateSerializer)
def create_cita_agil(request, data: Cita):
    # base
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
    cita.celular = data.celular
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
    # base
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
    return data.id, status.HTTP_200_OK


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cita_confirmar(request):
    cita_id = request.GET.get("id")
    citas = Cita.objects.filter(
        id=cita_id, is_deleted=False, estado=EstadoCita.PENDIENTE
    )
    if citas.__len__() == 0:
        return Response(
            ERROR_MESSAGE(
                tipo=citas.model.__name__,
                message="La cita pendiente no se ha encontrado",
                url=request.get_full_path(),
                fields_errors={"DoesNotExist": "id de la cita no existe"},
            ),
            status=status.HTTP_404_NOT_FOUND,
        )
    cita = citas[0]
    cita.estado = EstadoCita.CONFIRMADO
    cita.fechaConfirmacion = datetime.datetime.now()
    # base
    cita.updated_by = request.user

    cita.save()

    return Response(
        SUCCESS_MESSAGE(
            tipo=type(cita).__name__,
            message="Cita Confirmada",
            url=request.get_full_path(),
            data=True,
        ),
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cita_iniciar(request):
    cita_id = request.GET.get("id")
    citas = Cita.objects.filter(
        id=cita_id, is_deleted=False, estado=EstadoCita.CONFIRMADO
    )
    if citas.__len__() == 0:
        return Response(
            ERROR_MESSAGE(
                tipo=citas.model.__name__,
                message="La cita confirmada no se ha encontrado",
                url=request.get_full_path(),
                fields_errors={"DoesNotExist": "id de la cita no existe"},
            ),
            status=status.HTTP_404_NOT_FOUND,
        )
    cita = citas[0]
    cita.estado = EstadoCita.ATENDIENDO
    cita.fechaInicio = datetime.datetime.now()
    # base
    cita.updated_by = request.user
    cita.save()

    return Response(
        SUCCESS_MESSAGE(
            tipo=type(cita).__name__,
            message="Cita Iniciada",
            url=request.get_full_path(),
            data=True,
        ),
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cita_finalizar(request):
    cita_id = request.GET.get("id")
    citas = Cita.objects.filter(
        id=cita_id, is_deleted=False, estado=EstadoCita.ATENDIENDO
    )
    if citas.__len__() == 0:
        return Response(
            ERROR_MESSAGE(
                tipo=citas.model.__name__,
                message="La cita atendida no se ha encontrado",
                url=request.get_full_path(),
                fields_errors={"DoesNotExist": "id de la cita no existe"},
            ),
            status=status.HTTP_404_NOT_FOUND,
        )
    cita = citas[0]
    cita.estado = EstadoCita.FINALIZADO
    cita.fechaFin = datetime.datetime.now()
    # base
    cita.updated_by = request.user
    cita.save()

    return Response(
        SUCCESS_MESSAGE(
            tipo=type(cita).__name__,
            message="Cita Iniciada",
            url=request.get_full_path(),
            data=True,
        ),
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cita_validar(request):
    cita_id = request.GET.get("id")
    citas = Cita.objects.filter(
        id=cita_id,
        is_deleted=False,
        estado__in=[EstadoCita.FINALIZADO, EstadoCita.CONFIRMADO],
    )
    if citas.__len__() == 0:
        return Response(
            ERROR_MESSAGE(
                tipo=citas.model.__name__,
                message="La cita finalizada no se ha encontrado",
                url=request.get_full_path(),
                fields_errors={"DoesNotExist": "id de la cita no existe"},
            ),
            status=status.HTTP_404_NOT_FOUND,
        )
    cita = citas[0]
    cita.estado = EstadoCita.VALIDADO
    cita.fechaValidacion = datetime.datetime.now()
    # base
    cita.updated_by = request.user
    cita.save()

    return Response(
        SUCCESS_MESSAGE(
            tipo=type(cita).__name__,
            message="Cita Iniciada",
            url=request.get_full_path(),
            data=True,
        ),
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cita_list_filter(request):
    doctor_id = request.query_params.get("doctor_id")
    tipo = request.query_params.get("tipo")
    ubicacion_id = request.query_params.get("ubicacion_id")

    fecha = request.query_params.get("date")
    # tiene que ser el inicio de la semana
    semana = request.query_params.get("week")
    mes = request.query_params.get("month")
    kwargs = {}
    if ubicacion_id:
        kwargs["ubicacion_id"] = ubicacion_id
    if doctor_id:
        kwargs["doctor_id"] = doctor_id
    if tipo:
        kwargs["tipo"] = tipo

    if fecha:

        citas = Cita.objects.filter(fechaHoraCita__date=fecha)
        filter = "por fecha"
    elif semana:
        fecha_inicio_semana = datetime.datetime.strptime(semana, "%Y-%m-%d").date()

        fecha_fin_semana = fecha_inicio_semana + datetime.timedelta(days=6)
        citas = Cita.objects.filter(
            **kwargs,
            fechaHoraCita__range=[fecha_inicio_semana, fecha_fin_semana],
        )
        filter = "por semana"
    elif mes:
        fecha_inicio_mes = datetime.datetime.strptime(mes, "%Y-%m").date()
        fecha_fin_mes = fecha_inicio_mes.replace(
            year=fecha_inicio_mes.year + (1 if fecha_inicio_mes.month == 12 else 0),
            day=1,
            month=(1 if fecha_inicio_mes.month == 12 else fecha_inicio_mes.month + 1),
        ) - datetime.timedelta(days=1)
        citas = Cita.objects.filter(
            **kwargs, fechaHoraCita__range=[fecha_inicio_mes, fecha_fin_mes]
        )
        filter = "por mes"
    else:
        citas = Cita.objects.filter(**kwargs)
        filter = "todo"

    serializer = CitaResponseSerializer(citas, many=True)
    return Response(
        SUCCESS_MESSAGE(
            tipo=type(citas).__name__,
            message="Citas " + filter,
            url=request.get_full_path(),
            data=serializer.data,
        ),
        status=status.HTTP_200_OK,
    )
