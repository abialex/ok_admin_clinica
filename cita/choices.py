from django.db import models


class EstadoCita(models.IntegerChoices):
    PENDIENTE = 1, "Pendiente"
    CONFIRMADO = 2, "Confirmado"
    ATENDIENDO = 3, "Atendiendo"
    CONCLUIDO = 4, "Concluido"
    CANCELADO = 5, "Cancelado"


class TipoCita(models.IntegerChoices):
    TENTATIVA = 1, "Tentativa"
    AGIL = 2, "Agil"
    COMPLETA = 3, "Completa"
    OCUPADO = 4, "Ocupado"
