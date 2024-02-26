from django.urls import path
from cita.routers import router

app_name = "cita"

urlpatterns = []

urlpatterns += router.urls
