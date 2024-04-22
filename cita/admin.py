from django.contrib import admin

from cita.models import Cita
from shared.utils.baseModel import BaseModelAdmin


# Register your models here.
@admin.register(Cita)
class DoctorAdmin(BaseModelAdmin):
    list_display = ("razon", "doctor", "fechaHoraCita", "estado")


# @admin.register(CitaAgil)
# class DoctorAdmin(BaseModelAdmin):
#     list_display = ("razon", "doctor", "fechaHoraCita", "estado")


# @admin.register(CitaTentativa)
# class DoctorAdmin(BaseModelAdmin):
#     list_display = ("razon", "doctor", "fechaHoraCita", "estado")


# @admin.register(CitaCompleta)
# class DoctorAdmin(BaseModelAdmin):
#     list_display = ("razon", "doctor", "fechaHoraCita", "estado")
