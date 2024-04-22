from rest_framework import serializers

from recursos_humanos.choices import TipoAsistente
from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from recursos_humanos.serializers import PersonaSerializer
from session.serializers import UserResponseSerializer
from shared.utils.Global import EXCLUDE_ATTR
from ubicacion.models import Ubicacion


# --- INICIO DEL BLOQUE: Asistente CRUDs ---
class AsistenteCreateSerializer(PersonaSerializer):
    especialidad = serializers.CharField(max_length=100, required=False)
    ubicacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Ubicacion.objects.filter(is_active=True)
    )
    tipo = serializers.ChoiceField(choices=TipoAsistente.choices)


class AsistenteUpdateSerializer(PersonaSerializer):
    # id = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)
    ubicacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Ubicacion.objects.filter(is_active=True)
    )
    tipo = serializers.ChoiceField(choices=TipoAsistente.choices)


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Asistente Response ---
class AsistenteResponseSerializer(serializers.ModelSerializer):
    usuario = UserResponseSerializer()

    class Meta:
        model = Asistente
        exclude = EXCLUDE_ATTR


class AsistentesResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)
    tipo_string = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Asistente
        fields = (
            "id",
            "usuario_id",
            "username",
            "nombres",
            "apellidos",
            "dni",
            "tipo",
            "tipo_string",
            "estado",
        )

    def get_tipo_string(self, instance: Asistente):
        return TipoAsistente(instance.tipo).label

    def get_estado(self, instance: Asistente):
        return True if instance.is_active else False


# --- FIN DEL BLOQUE ---
