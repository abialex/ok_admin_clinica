from django.urls import path
from recursos_humanos.routers import router

app_name = "recursos_humanos"

urlpatterns = []

urlpatterns += router.urls
