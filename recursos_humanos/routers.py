from rest_framework.routers import DefaultRouter
from recursos_humanos.views import AsistenteViewSet, DoctorViewSet, PacienteViewSet
from shared.views import FotoPacienteViewSet

router = DefaultRouter()
router.register(r"paciente_foto", FotoPacienteViewSet, basename="paciente_foto")
