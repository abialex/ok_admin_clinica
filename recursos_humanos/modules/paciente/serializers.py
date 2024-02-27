from rest_framework import serializers
from recursos_humanos.models import Asistente, Paciente
from recursos_humanos.serializers import PersonaSerializer
from session.serializers import UserResponseSerializer
from shared.utils.Global import EXCLUDE_ATTR


# --- INICIO DEL BLOQUE: Paciente CRUDs ---
class PacienteCreateSerializer(PersonaSerializer):
    especialidad = serializers.CharField(max_length=100, required=False)


class PacienteUpdateSerializer(PersonaSerializer):
    id = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Paciente Response ---
class PacienteResponseSerializer(serializers.ModelSerializer):
    usuario = UserResponseSerializer()

    class Meta:
        model = Paciente
        exclude = EXCLUDE_ATTR


class PacientesResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Asistente
        fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# --- FIN DEL BLOQUE ---
