from rest_framework import serializers
from cita.choices import EstadoCita
from cita.models import CitaTentativa
from cita.serializers import CitaSerializer

from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from session.serializers import UserResponseSerializer
from shared.utils.Global import EXCLUDE_ATTR
from ubicacion.models import Ubicacion


# --- INICIO DEL BLOQUE: Doctor CRUDs ---
class CitaTentativaCreateSerializer(CitaSerializer):
    datosPaciente = serializers.CharField(max_length=150, required=True)
    celular = serializers.CharField(max_length=9, required=False)


class CitaTentativaUpdateSerializer(CitaSerializer):
    id = serializers.IntegerField()
    datosPaciente = serializers.CharField(max_length=150, required=True)
    celular = serializers.CharField(max_length=9, required=False)


# # --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Doctor Response ---
class CitaTentativaResponseSerializer(serializers.ModelSerializer):
    doctor_id = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    ubicacion_id = serializers.SerializerMethodField()
    ubicacion = serializers.SerializerMethodField()

    class Meta:
        model = CitaTentativa
        exclude = EXCLUDE_ATTR

    def get_doctor_id(self, instance: CitaTentativa):
        return instance.doctor.id

    def get_doctor(self, instance: CitaTentativa):
        return instance.doctor.nombres

    def get_ubicacion_id(self, instance: CitaTentativa):
        return instance.ubicacion.id

    def get_ubicacion(self, instance: CitaTentativa):
        return instance.ubicacion.nombre


class CitaTentativasResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = CitaTentativa
        exclude = ("doctor", "ubicacion") + EXCLUDE_ATTR


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: Asistente CRUDs ---
# class AsistenteCreateSerializer(PersonaSerializer):
#     especialidad = serializers.CharField(max_length=100, required=False)


# class AsistenteUpdateSerializer(PersonaSerializer):
#     id = serializers.IntegerField()
#     especialidad = serializers.CharField(max_length=100, required=False)


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: Asistente Response ---
# class AsistenteResponseSerializer(serializers.ModelSerializer):
#     usuario = UserResponseSerializer()

#     class Meta:
#         model = Asistente
#         fields = "__all__"


# class AsistentesResponseSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="usuario.username", read_only=True)

#     class Meta:
#         model = Asistente
#         fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: Paciente CRUDs ---
# class PacienteCreateSerializer(PersonaSerializer):
#     especialidad = serializers.CharField(max_length=100, required=False)


# class PacienteUpdateSerializer(PersonaSerializer):
#     id = serializers.IntegerField()
#     especialidad = serializers.CharField(max_length=100, required=False)


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: Paciente Response ---
# class PacienteResponseSerializer(serializers.ModelSerializer):
#     usuario = UserResponseSerializer()

#     class Meta:
#         model = Paciente
#         fields = "__all__"


# class PacientesResponseSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="usuario.username", read_only=True)

#     class Meta:
#         model = Asistente
#         fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# # --- FIN DEL BLOQUE ---
