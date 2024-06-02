from django.db import models


class TipoAsistente(models.IntegerChoices):
    ASISTENTE = 1, "Asistente"
    RECEPCION = 2, "Recepcion"
