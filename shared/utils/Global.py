import traceback
from enum import Enum
from cita.choices import EstadoCita
from cita.models import CitaAgil, CitaCompleta, CitaOcupada, CitaTentativa
from shared.models import ErrorLog


DIAS_TOKEN = 7
class RolEnum(Enum):
    DEVELOPER = 0
    ADMINISTRADOR = 1
    SUPERDOCTOR = 3
    DOCTOR = 4
    ASISTENTE = 5
    PACIENTE = 6


class CitaEnum(Enum):
    OCUPADA = 0
    TENTATIVA = 1
    AGIL = 3
    COMPLETA = 4


def ERROR_MESSAGE_LOG(name_file, message):
    return {"file": name_file, "message": message}


def ERROR_MESSAGE(tipo, message, url, fields_errors=None):
    return {
        "tipo": tipo,
        "message": message,
        "field_errors": fields_errors,
        "url": url,
    }


def SECCUSSFULL_MESSAGE(tipo, message, url, data):
    return {
        "tipo": tipo,
        "message": message,
        "url": url,
        "data": data,
    }


def es_paciente(user, rol):
    # Aquí puedes realizar múltiples operaciones
    if hasattr(user, rol):
        # Supongamos que queremos hacer algo más además de comprobar el atributo
        paciente = user.paciente
        return paciente.alguna_otra_operacion()  # Esto es solo un ejemplo
    return False


TABLA_ROL = {
    RolEnum.PACIENTE: [
        lambda user: hasattr(user, "paciente"),
        lambda user: user.paciente,
    ],
    RolEnum.DOCTOR: [lambda user: hasattr(user, "doctor"), lambda user: user.doctor],
    RolEnum.ASISTENTE: [
        lambda user: hasattr(user, "asistente"),
        lambda user: user.asistente,
    ],
    RolEnum.SUPERDOCTOR: [
        lambda user: hasattr(user, "susperdoctor"),
        lambda user: user.susperdoctor,
    ],
    RolEnum.ADMINISTRADOR: [
        lambda user: hasattr(user, "administrador"),
        lambda user: user.administrador,
    ],
    RolEnum.DEVELOPER: [
        lambda user: hasattr(user, "developer"),
        lambda user: user.developer,
    ],
}

def GET_ROL(user):
    for rol, funcionList in TABLA_ROL.items():
        # lambda user tiene el atributo rol
        if funcionList[0](user):
            # lambda user devuelve el objeto rol
            return rol, funcionList[1](user)

    return "Sin rol", user

TABLA_TIPO_CITA = {
    CitaEnum.OCUPADA: [
        lambda cita: isinstance(cita, CitaOcupada),
        lambda cita: cita.razonOcupado,
    ],
    CitaEnum.TENTATIVA: [
        lambda cita: isinstance(cita, CitaTentativa),
        lambda cita: "Estado: "
        + next(
            filter(lambda miembro: miembro.value == cita.estado, EstadoCita),
            None,
        ).name,
    ],
    CitaEnum.AGIL: [
        lambda cita: isinstance(cita, CitaAgil),
        lambda cita: cita.datosPaciente,
    ],
    CitaEnum.COMPLETA: [
        lambda cita: isinstance(cita, CitaCompleta),
        lambda cita: cita.paciente.id,
    ],
}


def GET_TIPO_CITA(cita):
    for tipo, funcionList in TABLA_TIPO_CITA.items():
        # lambda user tiene el atributo rol
        if funcionList[0](cita):
            # lambda user devuelve el objeto rol
            return tipo  # , funcionList[1](cita)

    return "Sin rol"  # , cita


def GET_ESTADO_CITA(estado):
    return next(
        filter(lambda miembro: miembro.value == estado, EstadoCita),
        None,
    ).name


def STRING(atributo):
    return atributo.field.attname


def LOGGING_SAVE(exc, url):
    tb_info = traceback.extract_tb(exc.__traceback__)
    file_name_error = "--"
    if tb_info:
        file_name_error = tb_info[-1].filename

    ErrorLog.objects.create(
        tipo=type(exc).__name__,
        mensaje=str(exc),
        url=url,
        archivo=file_name_error,
    )


TIPO_ERRORS = {
    "Http404": {"Http404": "no se encontró el objeto."},
    "MethodNotAllowed": {"MethodNotAllowed": "método no soportado"},
    "AuthenticationFailed": {"token": "Token inválido."},
    "NotAuthenticated": {"authentication": "An authorization token is not provided."},
    "InvalidToken": {"token": "An authorization token is not valid."},
    "IntegrityError": {"integrityError": "Esta acción vulvera un restricción"},
    "ValidationError": {"ValidationError": "Los campos no están completos"},
    # Add more handlers as needed
}
