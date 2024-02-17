from rest_framework import serializers

from recursos_humanos.models import Persona, Doctor
from session.serializers import UserResponseSerializer

# --- INICIO DEL BLOQUE: BASE ---
class PersonaSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=8)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=200)
    celular = serializers.CharField(max_length=9)
    domicilio = serializers.CharField(max_length=150, required=False)
    fechaNacimiento = serializers.CharField(max_length=12)
# --- FIN DEL BLOQUE ---

# --- INICIO DEL BLOQUE: CRUDs ---
class DoctoCreateSerializer(PersonaSerializer):
    especialidad = serializers.CharField(max_length=100, required=False)


class DoctorUpdateSerializer(PersonaSerializer):
    id = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)
# --- FIN DEL BLOQUE ---

# --- INICIO DEL BLOQUE: Response ---
class DoctorResponseSerializer(serializers.ModelSerializer):
    usuario = UserResponseSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorsResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = Doctor
        fields = ("id", "usuario_id", "username", "nombres", "apellidos")
# --- FIN DEL BLOQUE ---
