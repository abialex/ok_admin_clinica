from rest_framework import serializers
from cita.choices import EstadoCitaTentativa

from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from session.serializers import UserResponseSerializer
from ubicacion.models import Ubicacion


# --- INICIO DEL BLOQUE: BASE ---
class CitaSerializer(serializers.Serializer):
    razon = serializers.CharField(max_length=150, required=False)
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.filter(is_active=True),
        source="doctor",
        required=True,
    )

    ubicacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Ubicacion.objects.all(),
        source="ubicacion",
        required=True,
    )
    fechaHoraCita = serializers.DateTimeField()
    estado = serializers.ChoiceField(
        choices=EstadoCitaTentativa.choices,
    )


# --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: Doctor CRUDs ---
class CitaOcupadoCreateSerializer(CitaSerializer):
    razonOcupado = serializers.CharField(max_length=150, required=False)


# class DoctorUpdateSerializer(PersonaSerializer):
#     id = serializers.IntegerField()
#     especialidad = serializers.CharField(max_length=100, required=False)


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: Doctor Response ---
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
