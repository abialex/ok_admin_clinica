
from django.db import models
from django.utils import timezone


class ErrorLog(models.Model):
    tipo = models.CharField(max_length=40)
    mensaje = models.TextField()
    url = models.URLField()
    archivo = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        formatted_date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return f"{self.tipo} - {formatted_date}"