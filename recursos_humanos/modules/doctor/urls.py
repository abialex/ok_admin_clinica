from django.urls import path
from rest_framework.routers import DefaultRouter
from recursos_humanos.modules.doctor.views import (
    DoctorViewSet,
    doctor_get_by_ubicacion,
)


app_name = "doctor"
router = DefaultRouter()
router.register(r"doctor", DoctorViewSet, basename="doctor")

urlpatterns = [
    path(r"by-ubicacion", doctor_get_by_ubicacion),
]

urlpatterns += router.urls
