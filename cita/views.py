from rest_framework import status
from cita.common import CitaModel
from cita.models import CitaAgil, CitaCompleta, CitaOcupada, CitaTentativa
from cita.serializers import CitaByFechaIdUbicacionIdDoctor
from shared.utils.Global import ERROR_MESSAGE, SECCUSSFULL_MESSAGE
from shared.utils.baseModel import BaseModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from shared.utils.Global import ERROR_MESSAGE, GET_ROL, SECCUSSFULL_MESSAGE, RolEnum
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cita_by_fecha_iddoctor_idubicacion(request):
    result_serializer = CitaByFechaIdUbicacionIdDoctor(data=request.data)
    if result_serializer.is_valid():
        fechaHoraCita = result_serializer.data["fechaHoraCita"]
        doctor_id = result_serializer.data["doctor_id"]
        ubicacion_id = result_serializer.data["ubicacion_id"]

        citas_ocupadas = CitaOcupada.objects.filter(
            fechaHoraCita__date=fechaHoraCita,
            doctor_id=doctor_id,
            ubicacion_id=ubicacion_id,
        )

        citas_agiles = CitaAgil.objects.filter(
            fechaHoraCita__date=fechaHoraCita,
            doctor_id=doctor_id,
            ubicacion_id=ubicacion_id,
        )

        citas_tentativas = CitaTentativa.objects.filter(
            fechaHoraCita__date=fechaHoraCita,
            doctor_id=doctor_id,
            ubicacion_id=ubicacion_id,
        )

        citas_completas = CitaCompleta.objects.filter(
            fechaHoraCita__date=fechaHoraCita,
            doctor_id=doctor_id,
            ubicacion_id=ubicacion_id,
        )

        citas = []
        citas_completas_mapeadas = list(
            map(CitaModel.crear_cita_modelo, citas_completas)
        )
        citas_tentativas_mapeadas = list(
            map(CitaModel.crear_cita_modelo, citas_tentativas)
        )
        citas_ocupadas_mapeadas = list(map(CitaModel.crear_cita_modelo, citas_ocupadas))

        citas_agiles_mapeadas = list(map(CitaModel.crear_cita_modelo, citas_agiles))
        citas = (
            citas_completas_mapeadas
            + citas_tentativas_mapeadas
            + citas_ocupadas_mapeadas
            + citas_agiles_mapeadas
        )
        citas = sorted(citas, key=lambda x: x["fechaHoraCita"])

        return Response(
            SECCUSSFULL_MESSAGE(
                tipo=type(int).__name__,
                message="Citas por Fecha, IdUbicacion y IdDoctor",
                url=request.get_full_path(),
                data=citas,
            ),
            status=status.HTTP_200_OK,
        )
    else:
        custom_response_data = ERROR_MESSAGE(
            tipo=type(int).__name__,
            message="error",
            url=request.get_full_path(),
            fields_errors=result_serializer.errors,
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)
