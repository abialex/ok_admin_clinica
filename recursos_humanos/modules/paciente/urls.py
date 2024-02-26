from django.urls import path
from recursos_humanos.modules.paciente.views import PacienteViewSet
from rest_framework.routers import DefaultRouter


app_name = "paciente"
router = DefaultRouter()
router.register(r"paciente", PacienteViewSet, basename="paciente")

urlpatterns = [
    # path("doctors/by-idubicacion", doctor_get_by_idubicacion),
]


urlpatterns += router.urls
