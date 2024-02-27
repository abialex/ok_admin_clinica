from rest_framework import serializers

from recursos_humanos.models import Doctor
from recursos_humanos.serializers import PersonaSerializer
from session.serializers import UserResponseSerializer
from shared.utils.Global import EXCLUDE_ATTR
from ubicacion.models import Ubicacion
from ubicacion.serializers import UbicacionsResponseSerializer


# --- INICIO DEL BLOQUE: Doctor CRUDs ---
class DoctorCreateSerializer(PersonaSerializer):
    especialidad = serializers.CharField(max_length=100, required=False)
    ubicaciones = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ubicacion.objects.filter(is_active=True)
    )


class DoctorUpdateSerializer(PersonaSerializer):
    id = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)
    ubicaciones = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ubicacion.objects.filter(is_active=True), required=False
    )


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Doctor Response ---
class DoctorResponseSerializer(serializers.ModelSerializer):
    usuario = UserResponseSerializer()
    ubicaciones = UbicacionsResponseSerializer(many=True)

    class Meta:
        model = Doctor
        exclude = EXCLUDE_ATTR


class DoctorsResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Doctor
        fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# --- FIN DEL BLOQUE ---
