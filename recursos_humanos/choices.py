from django.db import models


class TipoAsistente(models.IntegerChoices):
    ASISTENTE = 1, "Asistente"
    RECEPCION = 2, "Recepcion"


class TipoDoctor(models.IntegerChoices):
    DOCTOR = 1, "Doctor"
    ADMINISTRADOR = 2, "Administrador"
