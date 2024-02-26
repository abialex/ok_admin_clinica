from django.db import models


class EstadoCitaTentativa(models.IntegerChoices):
    CONFIRMADA = 1, "Confirmada"
    PENDIENTE = 2, "Pendiente"
    CANCELADA = 3, "Cancelada"
