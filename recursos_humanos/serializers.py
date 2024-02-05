from rest_framework import serializers

from recursos_humanos.models import Persona, Doctor


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class DoctorAgregateSerializer(serializers.ModelSerializer):
    usuario_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Doctor.objects.all(), source="doctor",
                                                    required=True)
    class Meta:
        model = Doctor
        fields = ('dni', 'nombres', 'apellidos', 'celular', 'usuario_id')
