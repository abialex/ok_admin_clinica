from rest_framework.routers import DefaultRouter
from recursos_humanos.views import DoctorViewSet
from shared.views import FotoPacienteViewSet

router = DefaultRouter()

router.register(r"doctor", DoctorViewSet, basename="doctor")
router.register(r"paciente_foto", FotoPacienteViewSet, basename="paciente_foto")
