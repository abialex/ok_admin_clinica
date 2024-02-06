from rest_framework.routers import DefaultRouter
from historia_clinica.views import HistoriaClinicaViewSet

router = DefaultRouter()

router.register(r'historia_clinica', HistoriaClinicaViewSet, basename="historia_clinica")
