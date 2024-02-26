from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shared.views import FotoPacienteViewSet

app_name = "recursos_humanos"

router = DefaultRouter()
router.register(r"paciente_foto", FotoPacienteViewSet, basename="paciente_foto")

urlpatterns = [
    path(
        "asistentes/",
        include("recursos_humanos.modules.asistente.urls", namespace="asistente"),
    ),
    path(
        "doctores/",
        include("recursos_humanos.modules.doctor.urls", namespace="doctor"),
    ),
    path(
        "pacientes/",
        include("recursos_humanos.modules.paciente.urls", namespace="paciente"),
    ),
]


# urlpatterns += router.urls
