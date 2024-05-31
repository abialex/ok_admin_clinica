from django.urls import path
from rest_framework.routers import DefaultRouter
from recursos_humanos.modules.doctor.views import (
    DoctorViewSet,
    doctor_activar,
    doctor_get_by_ubicacion,
    doctor_inactivar,
)


app_name = "doctor"
router = DefaultRouter()
router.register(r"doctor", DoctorViewSet, basename="doctor")

urlpatterns = [
    path(r"by-ubicacion", doctor_get_by_ubicacion),
    path("doctor-activar/by-id", doctor_activar),
    path("doctor-inactivar/by-id", doctor_inactivar),
]

urlpatterns += router.urls
