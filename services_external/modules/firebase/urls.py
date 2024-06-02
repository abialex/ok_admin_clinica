from django.urls import path
from recursos_humanos.modules.asistente.views import AsistenteViewSet
from rest_framework.routers import DefaultRouter

from services_external.modules.firebase.views import createOrUpdateUserTokenFirebase


app_name = "firebase"
router = DefaultRouter()
# router.register(r"asistente", AsistenteViewSet, basename="asistente")

urlpatterns = [
    path("create-token", createOrUpdateUserTokenFirebase),
]


urlpatterns += router.urls
