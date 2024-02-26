from django.db.models.signals import pre_delete
from django.dispatch import receiver
from back_hcl import settings
from django.db import models

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


class Doctor(Persona):
    especialidad = models.CharField(max_length=50, null=True, blank=True)
    ubicaciones = models.ManyToManyField(Ubicacion)
    # Otros campos específicos de doctores


@receiver(pre_delete, sender=Ubicacion)
def eliminar_ubicaciones_relacionadas(sender, instance, **kwargs):
    print("ejecutando relacion eliminacion")
    # Eliminar todos los libros relacionados con el autor que se está eliminando
    instance.ubicacion_set.all().delete()


class Asistente(Persona):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=False)
    rol = models.CharField(max_length=50)
    # Otros campos específicos de asistentes


class Paciente(Persona):
    historial_medico = models.CharField(max_length=50, null=True, blank=True)
    # Otros campos específicos de pacientes
