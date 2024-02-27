from rest_framework import serializers
from cita.choices import EstadoCita
from cita.models import CitaCompleta
from cita.serializers import CitaSerializer

from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from session.serializers import UserResponseSerializer
from shared.utils.Global import EXCLUDE_ATTR
from ubicacion.models import Ubicacion


# --- INICIO DEL BLOQUE: CitaCompleta CRUDs ---
class CitaCompletaCreateSerializer(CitaSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.filter(is_active=True),
        source="paciente",
        required=True,
    )


class CitaCompletaUpdateSerializer(CitaSerializer):
    id = serializers.IntegerField()
    paciente_id = serializers.PrimaryKeyRelatedField(
        queryset=Paciente.objects.filter(is_active=True),
        source="paciente",
        required=True,
    )


# # --- FIN DEL BLOQUE ---


# --- INICIO DEL BLOQUE: CitaCompleta Response ---
class CitaCompletaResponseSerializer(serializers.ModelSerializer):
    doctor_id = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    ubicacion_id = serializers.SerializerMethodField()
    ubicacion = serializers.SerializerMethodField()
    paciente_id = serializers.SerializerMethodField()
    paciente = serializers.SerializerMethodField()

    class Meta:
        model = CitaCompleta
        exclude = EXCLUDE_ATTR

    def get_doctor_id(self, instance: CitaCompleta):
        return instance.doctor.id

    def get_doctor(self, instance: CitaCompleta):
        return instance.doctor.nombres

    def get_ubicacion_id(self, instance: CitaCompleta):
        return instance.ubicacion.id

    def get_ubicacion(self, instance: CitaCompleta):
        return instance.ubicacion.nombre

    def get_paciente_id(self, instance: CitaCompleta):
        return instance.paciente.id

    def get_paciente(self, instance: CitaCompleta):
        return instance.paciente.nombres + " " + instance.paciente.apellidos


class CitaCompletasResponseSerializer(serializers.ModelSerializer):
    paciente_id = serializers.SerializerMethodField()
    paciente = serializers.SerializerMethodField()

    class Meta:
        model = CitaCompleta
        exclude = ("doctor", "ubicacion") + EXCLUDE_ATTR

    def get_paciente_id(self, instance: CitaCompleta):
        return instance.paciente.id

    def get_paciente(self, instance: CitaCompleta):
        return instance.paciente.nombres + " " + instance.paciente.apellidos


# --- FIN DEL BLOQUE ---


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
