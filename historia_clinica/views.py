from rest_framework import status
from rest_framework.response import Response

from historia_clinica.models import HistoriaClinica
from historia_clinica.serializers import HistoriaClinicaSerializer, HistoriaClinicasSerializer
from rest_framework.viewsets import ModelViewSet

from shared.utils.Global import SECCUSSFULL_MESSAGE
from shared.utils.baseModel import BaseModelViewSet

# Create your views here.
class HistoriaClinicaViewSet(BaseModelViewSet):
    queryset = HistoriaClinica.objects.filter(is_deleted=False)
    serializer_class = HistoriaClinicaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = HistoriaClinicasSerializer(queryset, many=True)
        custom_data = SECCUSSFULL_MESSAGE(
            tipo=type(self).__name__,
            message="lista de historias clinicas",
            url=request.get_full_path(),
        data=serializer.data
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(response).__name__,
            message="historia clinica creada",
            url=request.get_full_path(),
            data=response.data["id"],
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="historia clinica modificada",
            url=request.get_full_path(),
            data=response.data["id"]
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="historia clinica",
            url=request.get_full_path(),
            data=serializer.data
        )
        return Response(custom_response_data, status=status.HTTP_200_OK)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí puedes realizar acciones personalizadas al inicializar el ViewSet
        self.initialize_custom_logic()

    def initialize_custom_logic(self):
        # Agrega lógica personalizada que deseas realizar al inicializar el ViewSet
        pass
