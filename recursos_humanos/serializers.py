from rest_framework import serializers

from recursos_humanos.models import Asistente, Persona, Doctor
from session.serializers import UserResponseSerializer


# --- INICIO DEL BLOQUE: BASE ---
class PersonaSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=8)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=200)
    celular = serializers.CharField(max_length=9)
    domicilio = serializers.CharField(max_length=150, required=False)
    fechaNacimiento = serializers.CharField(max_length=12)
# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Doctor CRUDs ---
class DoctorCreateSerializer(PersonaSerializer):
    especialidad = serializers.CharField(max_length=100, required=False)


class DoctorUpdateSerializer(PersonaSerializer):
    id = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Doctor Response ---
class DoctorResponseSerializer(serializers.ModelSerializer):
    usuario = UserResponseSerializer()

    class Meta:
        model = Doctor
        fields = "__all__"


class DoctorsResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Doctor
        fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Asistente CRUDs ---
class AsistenteCreateSerializer(PersonaSerializer):
    especialidad = serializers.CharField(max_length=100, required=False)


class AsistenteUpdateSerializer(PersonaSerializer):
    id = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Asistente Response ---
class AsistenteResponseSerializer(serializers.ModelSerializer):
    usuario = UserResponseSerializer()

    class Meta:
        model = Asistente
        fields = "__all__"


class AsistentesResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Asistente
        fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# --- FIN DEL BLOQUE ---
