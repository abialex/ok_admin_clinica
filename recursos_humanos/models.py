from back_hcl import settings
from django.db import models

from shared.utils.baseModel import BaseModel


class Persona(BaseModel):
    dni = models.CharField(max_length=8, null=False, unique=True)
    nombres = models.CharField(max_length=100, null=False, blank=False)
    apellidos = models.CharField(max_length=200, null=False, blank=False)
    celular = models.CharField(max_length=9, null=True, blank=False)
    domicilio = models.CharField(max_length=150, null=True, blank=False)
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento", null=False)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )

    class Meta:
        abstract = True


class Doctor(Persona):
    especialidad = models.CharField(max_length=50, null=True)
    # Otros campos específicos de doctores


class Asistente(Persona):
    rol = models.CharField(max_length=50)
    # Otros campos específicos de asistentes


class Paciente(Persona):
    historial_medico = models.TextField()
    # Otros campos específicos de pacientes
