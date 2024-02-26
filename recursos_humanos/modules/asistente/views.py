from datetime import timezone
import datetime
from psycopg2 import IntegrityError

from recursos_humanos.models import Asistente, Doctor, Paciente
from recursos_humanos.modules.asistente.serializers import (
    AsistenteCreateSerializer,
    AsistenteResponseSerializer,
    AsistenteUpdateSerializer,
    AsistentesResponseSerializer,
)
from session.models import User
from shared.utils.Global import ERROR_MESSAGE, SECCUSSFULL_MESSAGE, STRING
from rest_framework import status
from shared.utils.baseModel import BaseModelViewSet
from django.db import transaction
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from shared.utils.decoradores import validar_serializer


# Create your views here.
class AsistenteViewSet(BaseModelViewSet):
    queryset = Asistente.objects.filter(is_active=True)
    # serializer_class = DoctoCreateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = AsistentesResponseSerializer(queryset, many=True)
        custom_data = SECCUSSFULL_MESSAGE(
            tipo=type(self).__name__,
            message="lista de Asistentes",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = AsistenteResponseSerializer(instance)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="Asistente",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    @validar_serializer(serializer=AsistenteCreateSerializer)
    def create(self, request, result_serializer, *args, **kwargs):
        with transaction.atomic():
            username = "slg_a_" + result_serializer.data[STRING(Asistente.dni)][:2]
            contrasenia = result_serializer.data[STRING(Asistente.dni)]
            if User.objects.filter(username=username).__len__() > 0:
                raise IntegrityError("Este username ya existe.")
            user = User.objects.create(
                username=username,
                password=make_password(contrasenia),
            )
            asistente = Asistente(
                nombres=result_serializer.data[STRING(Asistente.nombres)],
                apellidos=result_serializer.data[STRING(Asistente.apellidos)],
                dni=result_serializer.data[STRING(Asistente.dni)],
                celular=result_serializer.data[STRING(Asistente.celular)],
                fechaNacimiento=result_serializer.data[
                    STRING(Asistente.fechaNacimiento)
                ],
                ubicacion_id=result_serializer.data[STRING(Asistente.ubicacion)],
                usuario_id=user.id,
            )
            asistente.created_by = self.request.user
            asistente.save()

        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " creado",
            url=request.get_full_path(),
            data={
                "username": user.username,
                "contraseña": contrasenia,
            },
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)

    @validar_serializer(serializer=AsistenteUpdateSerializer)
    def update(self, request, result_serializer, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            instance.nombres = result_serializer.data[STRING(Asistente.nombres)]
            instance.apellidos = result_serializer.data[STRING(Asistente.apellidos)]
            instance.dni = result_serializer.data[STRING(Asistente.dni)]
            instance.celular = result_serializer.data[STRING(Asistente.celular)]
            instance.fechaNacimiento = result_serializer.data[
                STRING(Asistente.fechaNacimiento)
            ]
            instance.updated_at = datetime.datetime.now()
            instance.updated_by = self.request.user
            instance.save()

        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=self.queryset.model.__name__,
            message=self.queryset.model.__name__ + " modificado",
            url=request.get_full_path(),
            data=instance.id,
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)
