from django.db import models
from django.utils import timezone
from recursos_humanos.models import Paciente
from shared.utils.baseModel import BaseModel


class ErrorLog(models.Model):
    tipo = models.CharField(max_length=40)
    mensaje = models.TextField()
    url = models.URLField()
    archivo = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        formatted_date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.tipo} - {formatted_date}"


class Foto(BaseModel):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=False)
    imagen = models.ImageField(upload_to="paciente_imagenes", null=False)
    descripcion = models.CharField(max_length=300, null=True)
