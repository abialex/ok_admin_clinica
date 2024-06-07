from django.urls import path, include
from rest_framework.routers import DefaultRouter

# from cita.views import cita_by_fecha_iddoctor_idubicacion

from cita.views import (
    CitaViewSet,
    cita_by_fecha_iddoctor_idubicacion,
    cita_cancelar,
    cita_confirmar,
    cita_finalizar,
    cita_iniciar,
    cita_list_filter,
    cita_validar,
    create_cita_agil,
    update_cita_agil,
    create_cita_ocupado,
    update_cita_ocupado,
)
from shared.views import FotoPacienteViewSet

app_name = "cita"
router = DefaultRouter()
router.register(r"cita", CitaViewSet, basename="cita")

urlpatterns = [
    path("cita_agil_create", create_cita_agil),
    path("cita_agil_update", update_cita_agil),
    path("cita_ocupado_create", create_cita_ocupado),
    path("cita_ocupado_update", update_cita_ocupado),
    path("cita_ocupado_update", update_cita_ocupado),
    path("cita_confirmar/by-id", cita_confirmar),
    path("cita_iniciar/by-id", cita_iniciar),
    path("cita_finalizar/by-id", cita_finalizar),
    path("cita_validar/by-id", cita_validar),
    path("cita_cancelar/by-id", cita_cancelar),
    # path(
    #     "citas_completas/",
    #     include("cita.modules.cita_completa.urls", namespace="completa"),
    # ),
    # path(
    #     "citas_ocupadas/",
    #     include("cita.modules.cita_ocupada.urls", namespace="ocupada"),
    # ),
    # path(
    #     "citas_tentativas/",
    #     include("cita.modules.cita_tentativa.urls", namespace="tentativa"),
    # ),
    path(r"citas-by-fecha-iddoctor-idubicacion", cita_by_fecha_iddoctor_idubicacion),
    path(r"citas-list-filter-by-iddoctor/", cita_list_filter),
]
urlpatterns += router.urls
