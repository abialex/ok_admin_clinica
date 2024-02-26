from rest_framework import serializers
from cita.choices import EstadoCita
from cita.serializers import CitaSerializer

from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from session.serializers import UserResponseSerializer
from ubicacion.models import Ubicacion


# --- INICIO DEL BLOQUE: CitaAgil CRUDs ---
class CitaAgilCreateSerializer(CitaSerializer):
    datosPaciente = serializers.CharField(max_length=150, required=True)
    celular = serializers.CharField(max_length=9, required=False)


# class DoctorUpdateSerializer(PersonaSerializer):
#     id = serializers.IntegerField()
#     especialidad = serializers.CharField(max_length=100, required=False)


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: CitaAgil Response ---
# class DoctorResponseSerializer(serializers.ModelSerializer):
#     usuario = UserResponseSerializer()

#     class Meta:
#         model = Doctor
#         fields = "__all__"


# class DoctorsResponseSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="usuario.username", read_only=True)

#     class Meta:
#         model = Doctor
#         fields = ("id", "usuario_id", "username", "nombres", "apellidos")


# # --- FIN DEL BLOQUE ---
