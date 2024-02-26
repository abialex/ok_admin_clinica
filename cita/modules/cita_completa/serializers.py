from rest_framework import serializers
from cita.choices import EstadoCita
from cita.serializers import CitaSerializer

from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from session.serializers import UserResponseSerializer
from ubicacion.models import Ubicacion


# --- INICIO DEL BLOQUE: CitaCompleta CRUDs ---
class CitaCompletaCreateSerializer(CitaSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.filter(is_active=True),
        source="paciente",
        required=True,
    )


# class DoctorUpdateSerializer(PersonaSerializer):
#     id = serializers.IntegerField()
#     especialidad = serializers.CharField(max_length=100, required=False)


# # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: CitaCompleta Response ---
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
