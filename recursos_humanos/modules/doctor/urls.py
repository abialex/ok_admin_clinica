from django.urls import path
from rest_framework.routers import DefaultRouter
from recursos_humanos.modules.doctor.views import (
    DoctorViewSet,
    doctor_activar,
    doctor_get_by_ubicacion,
    doctor_get_by_user_doctor,
    doctor_inactivar,
    reset_password,
)


app_name = "doctor"
router = DefaultRouter()
router.register(r"doctor", DoctorViewSet, basename="doctor")

urlpatterns = [
    path(r"by-ubicacion", doctor_get_by_ubicacion),
    path("doctor-activar/by-id", doctor_activar),
    path("doctor-inactivar/by-id", doctor_inactivar),
    path("reset-password/by-id", reset_password),
    path("by-doctor_user", doctor_get_by_user_doctor),
]

urlpatterns += router.urls
