from shared.models import Foto
from rest_framework import serializers


class FotoPacienteSerializer(serializers.ModelSerializer):
    paciente_id = serializers.CharField(max_length=10)

    class Meta:
        model = Foto
        fields = ("id", "imagen", "paciente_id", "descripcion")
