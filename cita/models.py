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


class CitaAgil(Cita):
    datosPaciente = models.CharField(max_length=150, blank=False, null=False)
    celular = models.CharField(max_length=9, null=True)


class CitaTentativa(Cita):
    datosPaciente = models.CharField(max_length=150, blank=False, null=False)
    celular = models.CharField(max_length=9, null=True)


class CitaCompleta(Cita):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False)
