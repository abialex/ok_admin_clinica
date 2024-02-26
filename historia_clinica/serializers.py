from django.utils.datetime_safe import date
from rest_framework import serializers

from historia_clinica.models import HistoriaClinica

# --- INICIO DEL BLOQUE: **** ---
class HistoriaClinicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoriaClinica
        fields = '__all__'

class HistoriaClinicasSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoriaClinica
        fields = ('id','motivoConsulta', 'examenInterior', 'examenExterior' )
# --- FIN DEL BLOQUE ---
