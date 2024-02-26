from shared.models import Foto
from shared.serializers import FotoPacienteSerializer
from shared.utils.Global import SECCUSSFULL_MESSAGE, STRING
from rest_framework.response import Response
from shared.utils.baseModel import BaseModelViewSet
from rest_framework import status
from django.http import FileResponse
import uuid


# Create your views here.
class FotoPacienteViewSet(BaseModelViewSet):
    queryset = Foto.objects.filter(is_deleted=False)
    serializer_class = FotoPacienteSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(response).__name__,
            message="Foto creado",
            url=request.get_full_path(),
            data=response.data[STRING(Foto.id)],
        )
        return Response(custom_response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.validated_data[STRING(Foto.imagen)].name = str(uuid.uuid4()) + str(
            ".jpg"
        )
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        custom_data = SECCUSSFULL_MESSAGE(
            tipo=type(self).__name__,
            message="lista de historias clinicas",
            url=request.get_full_path(),
            data=serializer.data,
        )
        return Response(custom_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        custom_response_data = SECCUSSFULL_MESSAGE(
            tipo=type(int).__name__,
            message="historia clinica",
            url=request.get_full_path(),
            data=serializer.data,
        )
        with open(instance.imagen.path, "rb") as f:
            imagen_data = f.read()

        # Devuelve la imagen como una respuesta HTTP
        return FileResponse([imagen_data, imagen_data], content_type="image/jpeg")
