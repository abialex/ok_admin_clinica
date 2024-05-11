from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ubicacion.views import UbicacionViewSet


app_name = "ubicacion"

router = DefaultRouter()
router.register("ubicacion", UbicacionViewSet, basename="ubicacion")

urlpatterns = [
    # path(
    #     "asistentes/",
    #     include("recursos_humanos.modules.asistente.urls", namespace="asistente"),
    # ),
    # path(
    #     "doctores/",
    #     include("recursos_humanos.modules.doctor.urls", namespace="doctor"),
    # ),
    # path(
    #     "pacientes/",
    #     include("recursos_humanos.modules.paciente.urls", namespace="paciente"),
    # ),
]


urlpatterns += router.urls
