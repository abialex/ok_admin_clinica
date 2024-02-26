from django.urls import path
from recursos_humanos.modules.asistente.views import AsistenteViewSet
from rest_framework.routers import DefaultRouter


app_name = "asistente"
router = DefaultRouter()
router.register(r"asistente", AsistenteViewSet, basename="asistente")

urlpatterns = [
    # path("doctors/by-idubicacion", doctor_get_by_idubicacion),
]


urlpatterns += router.urls
