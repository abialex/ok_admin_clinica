from django.db import models

from shared.utils.baseModel import BaseModel


# Create your models here.
class HistoriaClinica(BaseModel):
    motivoConsulta = models.CharField(max_length=60, blank=False, null=False)
    examenInterior = models.CharField(max_length=60, blank=False, null=False)
    examenExterior = models.CharField(max_length=60, blank=False, null=False)
