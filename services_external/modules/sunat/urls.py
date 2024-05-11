from django.urls import path
from recursos_humanos.modules.asistente.views import AsistenteViewSet
from rest_framework.routers import DefaultRouter

from services_external.modules.sunat.views import getPersonaSunByDni


app_name = "sunat"
router = DefaultRouter()
# router.register(r"asistente", AsistenteViewSet, basename="asistente")

urlpatterns = [
    path("persona-dni/<str:dni>", getPersonaSunByDni),
]


urlpatterns += router.urls
