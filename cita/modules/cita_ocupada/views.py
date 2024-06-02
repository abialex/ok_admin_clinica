# from django.shortcuts import render
# from rest_framework import status
# from cita.models import CitaOcupada, CitaAgil, CitaTentativa, CitaCompleta
# from cita.modules.cita_ocupada.serializers import (
#     CitaOcupadoCreateSerializer,
#     CitaOcupadoResponseSerializer,
#     CitaOcupadoUpdateSerializer,
#     CitaOcupadosResponseSerializer,
# )
# from session.models import User
# from shared.utils.Global import ERROR_MESSAGE, SUCCESS_MESSAGE, STRING
# from shared.utils.baseModel import BaseModelViewSet
# from rest_framework.response import Response
# from django.db import transaction
# from psycopg2 import IntegrityError
# from django.contrib.auth.hashers import make_password
# import datetime

# from shared.utils.decoradores import validar_data_serializer, validar_serializer


# # Create your views here.
# class CitaOcupadaViewSet(BaseModelViewSet):
#     queryset = CitaOcupada.objects.filter(is_deleted=False)
#     # serializer_class = DoctoCreateSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = CitaOcupadosResponseSerializer(queryset, many=True)
#         custom_data = SUCCESS_MESSAGE(
#             tipo=self.queryset.model.__name__,
#             message=self.queryset.model.__name__ + " list",
#             url=request.get_full_path(),
#             data=serializer.data,
#         )
#         return Response(custom_data, status=status.HTTP_200_OK)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = CitaOcupadoResponseSerializer(instance)
#         custom_response_data = SUCCESS_MESSAGE(
#             tipo=self.queryset.model.__name__,
#             message=self.queryset.model.__name__ + " by-id",
#             url=request.get_full_path(),
#             data=serializer.data,
#         )
#         return Response(custom_response_data, status=status.HTTP_200_OK)

#     @validar_data_serializer(
#         from_dict=CitaOcupada.from_dict, serializer=CitaOcupadoCreateSerializer
#     )
#     def create(self, request, cls):
#         with transaction.atomic():
#             cls.created_by = self.request.user
#             cls.save()
#         return cls.id, "creado"

#     @validar_data_serializer(
#         from_dict=CitaOcupada.from_dict, serializer=CitaOcupadoUpdateSerializer
#     )
#     def update(self, request, cls: CitaOcupada, pk):
#         with transaction.atomic():
#             instance = self.get_object()
#             instance.razon = cls.razon
#             instance.doctor_id = cls.doctor.id
#             instance.ubicacion_id = cls.ubicacion.id
#             instance.fechaHoraCita = cls.fechaHoraCita
#             instance.razonOcupado = cls.razonOcupado
#             instance.estado = cls.estado
#             instance.updated_at = datetime.datetime.now()
#             instance.updated_by = self.request.user
#             instance.save()
#         return instance.id, "modificado"
