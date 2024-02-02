from django.db import models

from back_hcl.utils.baseModel import BaseModel


# Create your models here.
class HistoriaClinica(BaseModel):
    motivoConsulta = models.CharField(max_length=60, blank=False, null=False)
    examenInterior = models.CharField(max_length=60, blank=False, null=False)
    examenExterior = models.CharField(max_length=60, blank=False, null=False)

    def set_created_by_updated_by(sender, instance, *args, **kwargs):
        # Obtén el usuario autenticado desde la solicitud (request)
        user = instance.created_by  # Suponiendo que el usuario esté configurado previamente en la instancia
        print("sdsd")
        instance.updated_by = user