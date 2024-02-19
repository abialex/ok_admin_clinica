from django.db import transaction
from rest_framework import serializers

from recursos_humanos.models import Persona, Doctor
from session.dto import UserDTO
from session.models import User


class UserResponsiveSerializer(serializers.ModelSerializer):
    persona = serializers.CharField(read_only=True, source="persona.get_nombre_completo")
    sessionKey = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    sedes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', "persona", "sessionKey", "sedes", "roles")

    def get_sessionKey(self, obj):
        extra_data = self.context.get('extra_data', {})
        return extra_data.get('sessionKey', None)

    def get_sedes(self, obj):
        extra_data = self.context.get('extra_data', {})
        return extra_data.get('sedes', None)

    def get_roles(self, obj):
        extra_data = self.context.get('extra_data', {})
        return extra_data.get('roles', None)

# --- INICIO DEL BLOQUE: **** ---
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class UserFormSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    dni = serializers.CharField(max_length=8)
    nombres = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=200)
    celular = serializers.CharField(max_length=9)
    domicilio = serializers.CharField(max_length=150, required=False)
    fechaNacimiento = serializers.CharField(max_length=12)

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
# --- FIN DEL BLOQUE ---


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=120, required=True)
