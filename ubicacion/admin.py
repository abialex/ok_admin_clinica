from django.contrib import admin

from shared.utils.baseModel import BaseModelAdmin
from .models import Ubicacion


# admin.site.register(ErrorLog)
@admin.register(Ubicacion)
class UbicacionAdmin(BaseModelAdmin):
    list_display = ("nombre", "direccion", "contacto_telefono", "contacto_email")
