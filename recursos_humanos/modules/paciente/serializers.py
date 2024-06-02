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
    usuario_id = serializers.SerializerMethodField()
    usuario_username = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        exclude = ("usuario",) + EXCLUDE_ATTR

    def get_usuario_id(self, instance: Paciente):
        return instance.usuario.id

    def get_usuario_username(self, instance: Paciente):
        return instance.usuario.username


class PacientesResponseSerializer(serializers.ModelSerializer):
    usuario_username = serializers.SerializerMethodField()

    class Meta:
        model = Paciente
        fields = (
            "id",
            "usuario_id",
            "usuario_username",
            "nombres",
            "apellidos",
            "dni",
            "celular",
        )

    def get_usuario_username(self, instance: Paciente):
        return instance.usuario.username


# --- FIN DEL BLOQUE ---
