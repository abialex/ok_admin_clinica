from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cita.views import cita_by_fecha_iddoctor_idubicacion

from shared.views import FotoPacienteViewSet

app_name = "cita"

urlpatterns = [
    path(
        "citas_agiles/",
        include("cita.modules.cita_agil.urls", namespace="agil"),
    ),
    path(
        "citas_completas/",
        include("cita.modules.cita_completa.urls", namespace="completa"),
    ),
    path(
        "citas_ocupadas/",
        include("cita.modules.cita_ocupada.urls", namespace="ocupada"),
    ),
    path(
        "citas_tentativas/",
        include("cita.modules.cita_tentativa.urls", namespace="tentativa"),
    ),
    path(r"citas-by-fecha-iddoctor-idubicacion", cita_by_fecha_iddoctor_idubicacion),
]
