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
    ubicaciones_id = serializers.PrimaryKeyRelatedField(
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
    usuario_id = serializers.SerializerMethodField()
    usuario_username = serializers.SerializerMethodField()
    ubicaciones = UbicacionsResponseSerializer(many=True)

    class Meta:
        model = Doctor
        exclude = ("usuario",) + EXCLUDE_ATTR

    def get_usuario_id(self, instance: Doctor):
        return instance.usuario.id

    def get_usuario_username(self, instance: Doctor):
        return instance.usuario.username


class DoctorsResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Doctor
        fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# --- FIN DEL BLOQUE ---
