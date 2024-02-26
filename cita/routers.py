from rest_framework.routers import DefaultRouter
from cita.views import CitaOcupadaViewSet

router = DefaultRouter()

router.register(r"cita_ocupada", CitaOcupadaViewSet, basename="cita_ocupada")
