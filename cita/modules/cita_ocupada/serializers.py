# from rest_framework import serializers
# from cita.choices import EstadoCita
# from cita.models import CitaOcupada
# from cita.serializers import CitaSerializer

# from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
# from session.serializers import UserResponseSerializer
# from shared.utils.Global import EXCLUDE_ATTR
# from ubicacion.models import Ubicacion


# # --- INICIO DEL BLOQUE: Doctor CRUDs ---
# class CitaOcupadoCreateSerializer(CitaSerializer):
#     razonOcupado = serializers.CharField(max_length=150, required=False)


# class CitaOcupadoUpdateSerializer(CitaSerializer):
#     id = serializers.IntegerField()
#     razonOcupado = serializers.CharField(max_length=150, required=False)


# # # --- FIN DEL BLOQUE ---


# # # --- INICIO DEL BLOQUE: Doctor Response ---
# class CitaOcupadoResponseSerializer(serializers.ModelSerializer):
#     doctor_id = serializers.SerializerMethodField()
#     doctor = serializers.SerializerMethodField()
#     ubicacion_id = serializers.SerializerMethodField()
#     ubicacion = serializers.SerializerMethodField()

#     class Meta:
#         model = CitaOcupada
#         exclude = EXCLUDE_ATTR

#     def get_doctor_id(self, instance: CitaOcupada):
#         return instance.doctor.id

#     def get_doctor(self, instance: CitaOcupada):
#         return instance.doctor.nombres

#     def get_ubicacion_id(self, instance: CitaOcupada):
#         return instance.ubicacion.id

#     def get_ubicacion(self, instance: CitaOcupada):
#         return instance.ubicacion.nombre


# class CitaOcupadosResponseSerializer(serializers.ModelSerializer):
#     # doctor_id = serializers.SerializerMethodField()
#     # doctor = serializers.SerializerMethodField()
#     # ubicacion_id = serializers.SerializerMethodField()
#     # ubicacion = serializers.SerializerMethodField()

#     class Meta:
#         model = CitaOcupada
#         exclude = ("doctor", "ubicacion") + EXCLUDE_ATTR


# # # --- FIN DEL BLOQUE ---
