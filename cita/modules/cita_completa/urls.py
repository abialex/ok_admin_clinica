from django.urls import path
from rest_framework.routers import DefaultRouter
from cita.modules.cita_completa.views import CitaCompletaViewSet


app_name = "citas_completas"
router = DefaultRouter()
router.register(r"cita_completa", CitaCompletaViewSet, basename="cita_completa")

urlpatterns = [
    # path(r"by-ubicacion", doctor_get_by_ubicacion),
]

urlpatterns += router.urls
