from django.db import models
from cita.choices import EstadoCita, TipoCita
from recursos_humanos.models import Doctor, Paciente
from shared.utils.baseModel import BaseModel
from ubicacion.models import Ubicacion


class Cita(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.CASCADE, null=True, blank=True
    )
    fechaHoraCita = models.DateTimeField(blank=False, null=False)
    estado = models.IntegerField(choices=EstadoCita.choices)
    tipo = models.IntegerField(choices=TipoCita.choices)
    razon = models.CharField(max_length=200, blank=False, null=True)
    # Campos adicionales opcionales
    razonOcupado = models.CharField(max_length=100, blank=True, null=True)
    datosPaciente = models.CharField(max_length=150, blank=True, null=True)
    celular = models.CharField(max_length=9, blank=True, null=True)
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, null=True, blank=True
    )

    # Nuevos campos
    fechaConfirmacion = models.DateTimeField(
        null=True, blank=True, help_text="Fecha en que se confirmó la cita."
    )
    fechaValidacion = models.DateTimeField(
        null=True, blank=True, help_text="Fecha en que se validó la cita."
    )
    fechaInicio = models.DateTimeField(
        null=True, blank=True, help_text="Fecha de inicio de la cita."
    )
    fechaFin = models.DateTimeField(
        null=True, blank=True, help_text="Fecha de finalización de la cita."
    )

    @property
    def cita_info(self):
        # Formatea la información de la cita de forma más clara
        return f"{self.razon} a las {self.fechaHoraCita}"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id", None),
            razon=data.get("razon", None),
            doctor_id=data.get("doctor_id", None),
            ubicacion_id=data.get("ubicacion_id", None),
            fechaHoraCita=data.get("fechaHoraCita", None),
            estado=data.get("estado", None),
            tipo=data.get("tipo", None),
            razonOcupado=data.get("razonOcupado", None),
            datosPaciente=data.get("datosPaciente", None),
            celular=data.get("celular", None),
            paciente_id=data.get("paciente_id", None),
            # Nuevos campos
            fechaConfirmacion=data.get("fechaConfirmacion", None),
            fechaValidacion=data.get("fechaValidacion", None),
            fechaInicio=data.get("fechaInicio", None),
            fechaFin=data.get("fechaFin", None),
        )
