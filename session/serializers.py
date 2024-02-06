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
"""
    def update(self, instance, validated_data):

        instance.username=validated_data['username']
        print(instance.pk)
        instance.save()
        print("debajo")
        return instance

    def create(self, validated_data):
        with transaction.atomic():
            try:
                user_instance = User.objects.create(username=validated_data['username'])
                validated_data['user_id'] = user_instance.pk
                persona_instance = Doctor.objects.create(nombres=validated_data['nombres'],
                                                      apellidos=validated_data['apellidos'],
                                                      dni=validated_data['dni'],
                                                      celular=validated_data['celular'],
                                                       usuario_id=user_instance.pk,
                                                         fechaNacimiento="1997-02-03")
            except Exception as e:
                print(e)

        self.data["id"] = user_instance.pk
        return self

"""
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
