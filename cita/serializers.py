from rest_framework import serializers
from cita.choices import EstadoCita
from recursos_humanos.models import Doctor
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
        choices=EstadoCita.choices,
    )


# --- FIN DEL BLOQUE ---
class CitaByFechaIdUbicacionIdDoctorSerializer(serializers.Serializer):
    fechaHoraCita = serializers.DateField()
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
