import cita
from cita.choices import EstadoCita
from shared.utils.Global import CitaEnum


class CitaModel:

    def __init__(
        self,
        id,
        razon,
        doctor_id,
        ubicacion_id,
        ubicacion,
        fechaHoraCita,
        estado,
        estadoString,
        tipo,
        tipoString,
        celular,
        datosPaciente,
    ):
        self.id = id
        self.razon = razon
        self.doctor_id = doctor_id
        self.ubicacion = ubicacion
        self.ubicacion_id = ubicacion_id
        self.fechaHoraCita = fechaHoraCita
        self.estado = estado
        self.estadoString = estadoString
        self.tipo = tipo
        self.tipoString = tipoString
        self.celular = celular
        self.datosPaciente = datosPaciente

    def to_dict(self):
        return {
            "id": self.id,
            "razon": self.razon,
            "doctor_id": self.doctor_id,
            "ubicacion": self.ubicacion,
            "ubicacion_id": self.ubicacion_id,
            "fechaHoraCita": self.fechaHoraCita,
            "estado": self.estado,
            "estadoString": self.estadoString,
            "tipo": self.tipo,
            "tipoString": self.tipoString,
            "celular": self.celular,
            "datosPaciente": self.datosPaciente,
        }

    # def crear_cita_modelo(item):
    #     estadoString = GET_ESTADO_CITA(item.estado)
    #     tipo = GET_TIPO_CITA(item)
    #     match tipo:
    #         case CitaEnum.OCUPADA:
    #             datosPaciente = None
    #             celular = None
    #         case CitaEnum.TENTATIVA:
    #             datosPaciente = item.datosPaciente
    #             celular = item.celular
    #         case CitaEnum.AGIL:
    #             datosPaciente = item.datosPaciente
    #             celular = item.celular
    #         case CitaEnum.COMPLETA:
    #             datosPaciente = item.paciente.nombres + " " + item.paciente.apellidos
    #             celular = item.paciente.celular
    #         case _:
    #             raise ValueError("No se definió la cita: " + tipo.name)

    #     return CitaModel(
    #         id=item.id,
    #         razon=item.razon,
    #         doctor_id=item.doctor.id,
    #         ubicacion=item.ubicacion.nombre,
    #         ubicacion_id=item.ubicacion.id,
    #         fechaHoraCita=item.fechaHoraCita.strftime("%Y-%m-%d %H:%M:%S"),
    #         estado=item.estado,
    #         estadoString=estadoString,
    #         tipo=tipo.value,
    #         tipoString=tipo.name,
    #         celular=celular,
    #         datosPaciente=datosPaciente,
    #     ).to_dict()
