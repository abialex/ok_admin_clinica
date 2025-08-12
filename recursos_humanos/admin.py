from django.contrib import admin
from recursos_humanos.models import Administrador, Asistente, Doctor, Paciente
from shared.utils.baseModel import BaseModelAdmin


# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(BaseModelAdmin):
    list_display = ("nombres", "apellidos", "celular", "usuario")


@admin.register(Paciente)
class PacienteAdmin(BaseModelAdmin):
    list_display = ("nombres", "apellidos", "celular", "usuario")


@admin.register(Asistente)
class AsistenteAdmin(BaseModelAdmin):
    list_display = ("nombres", "apellidos", "celular", "usuario")


@admin.register(Administrador)
class AsistenteAdmin(BaseModelAdmin):
    list_display = ("nombres", "apellidos", "celular", "usuario")
