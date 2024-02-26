from django.db import models
from shared.utils.baseModel import BaseModel


# Create your models here.
class Ubicacion(BaseModel):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150, null=True)
    contacto_telefono = models.CharField(max_length=15, null=True)
    contacto_email = models.EmailField(max_length=150, null=True)

    def __str__(self):
        return self.nombre
