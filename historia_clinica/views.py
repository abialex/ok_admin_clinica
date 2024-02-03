from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from back_hcl.utils.baseModel import BaseModelViewSet
from historia_clinica.models import HistoriaClinica
from historia_clinica.serializers import HistoriaClinicaSerializer
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet


# Create your views here.
class CitasViewSet(ModelViewSet):
    queryset = HistoriaClinica.objects.filter(is_deleted=False)
    serializer_class = HistoriaClinicaSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí puedes realizar acciones personalizadas al inicializar el ViewSet
        self.initialize_custom_logic()

    def initialize_custom_logic(self):
        # Agrega lógica personalizada que deseas realizar al inicializar el ViewSet
        pass


