from django.urls import path
from rest_framework.routers import DefaultRouter

from cita.modules.cita_tentativa.views import CitaTentativaViewSet


app_name = "citas_tentativas"
router = DefaultRouter()
router.register(r"cita_tentativa", CitaTentativaViewSet, basename="cita_tentativa")

urlpatterns = [
    # path(r"by-ubicacion", doctor_get_by_ubicacion),
]

urlpatterns += router.urls
