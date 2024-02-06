from django.urls import path
from rest_framework.authtoken import views
from recursos_humanos.routers import router

app_name = "recursos_humanos"

urlpatterns = []

urlpatterns += router.urls
