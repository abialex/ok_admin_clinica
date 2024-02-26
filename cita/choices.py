from django.db import models


class EstadoCita(models.IntegerChoices):
    CONFIRMADA = 1, "Confirmada"
    PENDIENTE = 2, "Pendiente"
    CANCELADA = 3, "Cancelada"
