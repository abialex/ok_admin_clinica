# import datetime
# from rest_framework import status
# from cita.models import CitaCompleta
# from cita.modules.cita_completa.serializers import (
#     CitaCompletaCreateSerializer,
#     CitaCompletaResponseSerializer,
#     CitaCompletaUpdateSerializer,
#     CitaCompletasResponseSerializer,
# )
# from shared.utils.Global import ERROR_MESSAGE, SUCCESS_MESSAGE, STRING
# from shared.utils.baseModel import BaseModelViewSet
# from rest_framework.response import Response
# from django.db import transaction

# from shared.utils.decoradores import validar_data_serializer, validar_serializer


# # Create your views here.
# class CitaCompletaViewSet(BaseModelViewSet):
#     queryset = CitaCompleta.objects.filter(is_deleted=False)
#     # serializer_class = DoctoCreateSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = CitaCompletasResponseSerializer(queryset, many=True)
#         custom_data = SUCCESS_MESSAGE(
#             tipo=self.queryset.model.__name__,
#             message=self.queryset.model.__name__ + " list",
#             url=request.get_full_path(),
#             data=serializer.data,
#         )
#         return Response(custom_data, status=status.HTTP_200_OK)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = CitaCompletaResponseSerializer(instance)
#         custom_response_data = SUCCESS_MESSAGE(
#             tipo=self.queryset.model.__name__,
#             message=self.queryset.model.__name__ + " by-id",
#             url=request.get_full_path(),
#             data=serializer.data,
#         )
#         return Response(custom_response_data, status=status.HTTP_200_OK)

#     @validar_data_serializer(
#         from_dict=CitaCompleta.from_dict, serializer=CitaCompletaCreateSerializer
#     )
#     def create(self, request, cls):
#         with transaction.atomic():
#             cls.created_by = self.request.user
#             cls.save()
#         return cls.id, "creado"

#     @validar_data_serializer(
#         from_dict=CitaCompleta.from_dict, serializer=CitaCompletaUpdateSerializer
#     )
#     def update(self, request, cls: CitaCompleta, pk):
#         with transaction.atomic():
#             instance = self.get_object()
#             instance.razon = cls.razon
#             instance.doctor_id = cls.doctor.id
#             instance.ubicacion_id = cls.ubicacion.id
#             instance.fechaHoraCita = cls.fechaHoraCita
#             instance.paciente_id = cls.paciente.id
#             instance.estado = cls.estado
#             instance.updated_at = datetime.datetime.now()
#             instance.updated_by = self.request.user
#             instance.save()
#         return instance.id, "modificado"
