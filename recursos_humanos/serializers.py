from rest_framework import serializers

from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
from session.serializers import UserResponseSerializer
from ubicacion.models import Ubicacion
from ubicacion.serializers import UbicacionsResponseSerializer


# --- INICIO DEL BLOQUE: BASE ---
class PersonaSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=8)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=200)
    celular = serializers.CharField(max_length=9)
    domicilio = serializers.CharField(max_length=150, required=False)
    fechaNacimiento = serializers.CharField(max_length=12)


# --- FIN DEL BLOQUE ---
