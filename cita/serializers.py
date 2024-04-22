from rest_framework import serializers
from cita.choices import EstadoCita, TipoCita
from cita.models import Cita
from recursos_humanos.models import Doctor
from shared.utils.Global import EXCLUDE_ATTR
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


class CitaAgilCreateSerializer(CitaSerializer):
    datosPaciente = serializers.CharField(max_length=150, required=True)
    celular = serializers.CharField(max_length=9, required=False)
    tipo = serializers.ChoiceField(choices=TipoCita.choices, default=TipoCita.AGIL)
    estado = serializers.ChoiceField(
        choices=EstadoCita.choices, default=EstadoCita.PENDIENTE
    )


class CitaAgilUpdateSerializer(CitaSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Cita.objects.filter(is_active=True, tipo=TipoCita.AGIL),
        source="cita",
        required=True,
    )
    datosPaciente = serializers.CharField(max_length=150, required=True)
    celular = serializers.CharField(max_length=9, required=False)
    estado = serializers.ChoiceField(choices=EstadoCita.choices)


class CitaOcupadoCreateSerializer(CitaSerializer):

    razonOcupado = serializers.CharField(max_length=150, required=False)
    tipo = serializers.ChoiceField(choices=TipoCita.choices, default=TipoCita.OCUPADO)
    estado = serializers.ChoiceField(
        choices=EstadoCita.choices, default=EstadoCita.CONCLUIDO
    )


class CitaOcupadoUpdateSerializer(CitaSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Cita.objects.filter(is_active=True, tipo=TipoCita.OCUPADO),
        source="cita",
        required=True,
    )
    razonOcupado = serializers.CharField(max_length=150, required=False)
    estado = serializers.ChoiceField(
        choices=EstadoCita.choices, default=EstadoCita.CONCLUIDO
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


# # # --- INICIO DEL BLOQUE: Cita Response ---
class CitaResponseSerializer(serializers.ModelSerializer):
    doctor_id = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    ubicacion_id = serializers.SerializerMethodField()
    ubicacion = serializers.SerializerMethodField()
    estado_string = serializers.SerializerMethodField()
    tipo_string = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        exclude = EXCLUDE_ATTR

    def get_doctor_id(self, instance: Cita):
        return instance.doctor.id

    def get_doctor(self, instance: Cita):
        return instance.doctor.nombres

    def get_ubicacion_id(self, instance: Cita):
        return instance.ubicacion.id

    def get_ubicacion(self, instance: Cita):
        return instance.ubicacion.nombre

    def get_estado_string(self, instance: Cita):
        return EstadoCita(instance.estado).label

    def get_tipo_string(self, instance: Cita):
        return TipoCita(instance.tipo).label


class CitasResponseSerializer(serializers.ModelSerializer):
    # doctor_id = serializers.SerializerMethodField()
    # doctor = serializers.SerializerMethodField()
    # ubicacion_id = serializers.SerializerMethodField()
    # ubicacion = serializers.SerializerMethodField()
    estado_string = serializers.SerializerMethodField()
    tipo_string = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        exclude = ("doctor", "ubicacion") + EXCLUDE_ATTR

    def get_estado_string(self, instance: Cita):
        return EstadoCita(instance.estado).label

    def get_tipo_string(self, instance: Cita):
        return TipoCita(instance.tipo).label


# # # --- FIN DEL BLOQUE ---
