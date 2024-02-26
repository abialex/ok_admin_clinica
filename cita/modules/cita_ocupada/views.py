from django.shortcuts import render
from rest_framework import status
from cita.models import CitaOcupada, CitaAgil, CitaTentativa, CitaCompleta
from cita.modules.cita_ocupada.serializers import CitaOcupadoCreateSerializer
from session.models import User
from shared.utils.Global import ERROR_MESSAGE, SECCUSSFULL_MESSAGE, STRING
from shared.utils.baseModel import BaseModelViewSet
from rest_framework.response import Response
from django.db import transaction
from psycopg2 import IntegrityError
from django.contrib.auth.hashers import make_password
import datetime

from shared.utils.decoradores import validar_serializer


# Create your views here.
class CitaOcupadaViewSet(BaseModelViewSet):
    queryset = CitaOcupada.objects.filter(is_active=True)
    # serializer_class = DoctoCreateSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = PacientesResponseSerializer(queryset, many=True)
    #     custom_data = SECCUSSFULL_MESSAGE(
    #         tipo=type(self).__name__,
    #         message="lista de Pacientes",
    #         url=request.get_full_path(),
    #         data=serializer.data,
    #     )
    #     return Response(custom_data, status=status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = PacienteResponseSerializer(instance)
    #     custom_response_data = SECCUSSFULL_MESSAGE(
    #         tipo=type(int).__name__,
    #         message="Paciente",
    #         url=request.get_full_path(),
    #         data=serializer.data,
    #     )
    #     return Response(custom_response_data, status=status.HTTP_200_OK)
    @validar_serializer(serializer=CitaOcupadoCreateSerializer)
    def create(self, request, result_serializer, *args, **kwargs):
        with transaction.atomic():
            razonOcupado = (
                result_serializer.data[STRING(CitaOcupada.razonOcupado)]
                if result_serializer.data.get(STRING(CitaOcupada.razonOcupado))
                else None
            )
            razon = (
                result_serializer.data[STRING(CitaOcupada.razon)]
                if result_serializer.data.get(STRING(CitaOcupada.razon))
                else None
            )

            cita = CitaOcupada(
                razon=razon,
                doctor_id=result_serializer.data[STRING(CitaOcupada.doctor_id)],
                ubicacion_id=result_serializer.data[STRING(CitaOcupada.ubicacion_id)],
                fechaHoraCita=result_serializer.data[STRING(CitaOcupada.fechaHoraCita)],
                estado=result_serializer.data[STRING(CitaOcupada.estado)],
                razonOcupado=razonOcupado,
            )
            cita.created_by = self.request.user
            cita.save()

        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " creado",
            url=request.get_full_path(),
            data=cita.id,
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)

    # def update(self, request, *args, **kwargs):
    #     result_serializer = PacienteUpdateSerializer(data=request.data)
    #     if result_serializer.is_valid():
    #         with transaction.atomic():
    #             instance = self.get_object()
    #             instance.nombres = result_serializer.data["nombres"]
    #             instance.apellidos = result_serializer.data["apellidos"]
    #             instance.dni = result_serializer.data["dni"]
    #             instance.celular = result_serializer.data["celular"]
    #             instance.fechaNacimiento = result_serializer.data["fechaNacimiento"]
    #             instance.updated_at = datetime.datetime.now()
    #             instance.updated_by = self.request.user
    #             instance.save()

    #         custom_response_data = SECCUSSFULL_MESSAGE(
    #             tipo=type(int).__name__,
    #             message="Paciente Modificado",
    #             url=request.get_full_path(),
    #             data=instance.id,
    #         )
    #         return Response(custom_response_data, status=status.HTTP_201_CREATED)
    #     else:
    #         custom_response_data = ERROR_MESSAGE(
    #             tipo=type(int).__name__,
    #             message="error",
    #             url=request.get_full_path(),
    #             fields_errors=result_serializer.errors,
    #         )
    #         return Response(custom_response_data, status=status.HTTP_201_CREATED)
