from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shared.views import FotoPacienteViewSet

app_name = "recursos_humanos"

router = DefaultRouter()
# router.register(r"paciente_foto", FotoPacienteViewSet, basename="paciente_foto")

urlpatterns = [
    path(
        "firebase/",
        include("services_external.modules.firebase.urls", namespace="firebase"),
    ),
    # path(
    #     "doctores/",
    #     include("recursos_humanos.modules.doctor.urls", namespace="doctor"),
    # ),
]


# urlpatterns += router.urls
