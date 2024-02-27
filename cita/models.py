from django.db import models
from cita.choices import EstadoCita
from recursos_humanos.models import Doctor, Paciente
from shared.utils.baseModel import BaseModel
from ubicacion.models import Ubicacion


class Cita(BaseModel):
    razon = models.CharField(max_length=200, blank=False, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=False)
    fechaHoraCita = models.DateTimeField(blank=False, null=False)
    estado = models.IntegerField(
        choices=EstadoCita.choices,
        default=EstadoCita.PENDIENTE,
    )

    class Meta:
        abstract = True

    @property
    def cita_info(self):
        return self.razon + "a las" + self.fechaHoraCita


class CitaOcupada(Cita):
    razonOcupado = models.CharField(
        max_length=100, default="sin razón", blank=False, null=True
    )

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", None),
            razon=data.get("razon", None),
            doctor_id=data.get("doctor_id", None),
            ubicacion_id=data.get("ubicacion_id", None),
            fechaHoraCita=data.get("fechaHoraCita", None),
            estado=data.get("estado", None),
            razonOcupado=data.get("razonOcupado", "sin razón"),
        )


class CitaAgil(Cita):
    datosPaciente = models.CharField(max_length=150, blank=False, null=False)
    celular = models.CharField(max_length=9, null=True)
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", None),
            razon=data.get("razon", None),
            doctor_id=data.get("doctor_id", None),
            ubicacion_id=data.get("ubicacion_id", None),
            fechaHoraCita=data.get("fechaHoraCita", None),
            estado=data.get("estado", None),
            datosPaciente=data.get("datosPaciente", None),
            celular=data.get("celular", None),
        )


class CitaTentativa(Cita):
    datosPaciente = models.CharField(max_length=150, blank=False, null=False)
    celular = models.CharField(max_length=9, null=True)
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", None),
            razon=data.get("razon", None),
            doctor_id=data.get("doctor_id", None),
            ubicacion_id=data.get("ubicacion_id", None),
            fechaHoraCita=data.get("fechaHoraCita", None),
            estado=data.get("estado", None),
            datosPaciente=data.get("datosPaciente", None),
            celular=data.get("celular", None),
        )


class CitaCompleta(Cita):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", None),
            razon=data.get("razon", None),
            doctor_id=data.get("doctor_id", None),
            ubicacion_id=data.get("ubicacion_id", None),
            fechaHoraCita=data.get("fechaHoraCita", None),
            estado=data.get("estado", None),
            paciente_id=data.get("paciente_id", None),
        )
