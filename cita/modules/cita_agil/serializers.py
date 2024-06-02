# from rest_framework import serializers
# from cita.choices import EstadoCita
# from cita.models import CitaAgil
# from cita.serializers import CitaSerializer

# from recursos_humanos.models import Asistente, Paciente, Persona, Doctor
# from session.serializers import UserResponseSerializer
# from shared.utils.Global import EXCLUDE_ATTR
# from ubicacion.models import Ubicacion


# # --- INICIO DEL BLOQUE: CitaAgil CRUDs ---
# class CitaAgilCreateSerializer(CitaSerializer):
#     datosPaciente = serializers.CharField(max_length=150, required=True)
#     celular = serializers.CharField(max_length=9, required=False)


# class CitaAgilUpdateSerializer(CitaSerializer):
#     id = serializers.IntegerField()
#     datosPaciente = serializers.CharField(max_length=150, required=True)
#     celular = serializers.CharField(max_length=9, required=False)


# # # --- FIN DEL BLOQUE ---


# # --- INICIO DEL BLOQUE: CitaAgil Response ---
# class CitaAgilResponseSerializer(serializers.ModelSerializer):
#     doctor_id = serializers.SerializerMethodField()
#     doctor = serializers.SerializerMethodField()
#     ubicacion_id = serializers.SerializerMethodField()
#     ubicacion = serializers.SerializerMethodField()

#     class Meta:
#         model = CitaAgil
#         exclude = EXCLUDE_ATTR

#     def get_doctor_id(self, instance: CitaAgil):
#         return instance.doctor.id

#     def get_doctor(self, instance: CitaAgil):
#         return instance.doctor.nombres

#     def get_ubicacion_id(self, instance: CitaAgil):
#         return instance.ubicacion.id

#     def get_ubicacion(self, instance: CitaAgil):
#         return instance.ubicacion.nombre


# class CitaAgilsResponseSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CitaAgil
#         exclude = ("doctor", "ubicacion") + EXCLUDE_ATTR


# # --- FIN DEL BLOQUE ---
