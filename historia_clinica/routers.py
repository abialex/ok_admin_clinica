from rest_framework.routers import DefaultRouter
from historia_clinica.views import CitasViewSet

router = DefaultRouter()

router.register(r'hcl', CitasViewSet, basename="hcl")
