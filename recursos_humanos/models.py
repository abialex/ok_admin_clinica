from back_hcl import settings
from django.db import models
from recursos_humanos.choices import TipoAdministrador, TipoAsistente, TipoDoctor
from shared.utils.baseModel import BaseModel
from ubicacion.models import Ubicacion


class Persona(BaseModel):
    dni = models.CharField(max_length=8, null=False, unique=True)
    nombres = models.CharField(max_length=100, null=False, blank=False)
    apellidos = models.CharField(max_length=200, null=False, blank=False)
    celular = models.CharField(max_length=9, null=True, blank=False)
    domicilio = models.CharField(max_length=150, null=True, blank=True)
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=False)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Doctor(Persona):
    especialidad = models.CharField(max_length=50, null=True, blank=True)
    ubicaciones = models.ManyToManyField(Ubicacion)
    tipo = models.IntegerField(choices=TipoDoctor.choices, default=TipoDoctor.DOCTOR)
    # Otros campos específicos de doctores


class Asistente(Persona):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=False)
    tipo = models.IntegerField(choices=TipoAsistente.choices)
    # Otros campos específicos de asistentes


class Paciente(Persona):
    historial_medico = models.CharField(max_length=50, null=True, blank=True)


class Administrador(Persona):
    tipo = models.IntegerField(
        choices=TipoAdministrador.choices, default=TipoAdministrador.ASISTENTE
    )
    # Otros campos específicos de pacientes
