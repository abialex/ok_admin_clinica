from rest_framework.routers import DefaultRouter

from recursos_humanos.views import DoctorViewSet

router = DefaultRouter()

router.register(r"doctor", DoctorViewSet, basename="doctor")
