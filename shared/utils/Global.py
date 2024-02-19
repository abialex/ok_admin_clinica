import traceback

from shared.models import ErrorLog

DIAS_TOKEN = 7
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
    "PACIENTE": [lambda user: hasattr(user, "paciente"), lambda user: user.paciente],
    "DOCTOR": [lambda user: hasattr(user, "doctor"), lambda user: user.doctor],
    "ASISTENTE": [lambda user: hasattr(user, "asistente"), lambda user: user.asistente],
    "SUPERDOCTOR": [
        lambda user: hasattr(user, "susperdoctor"),
        lambda user: user.susperdoctor,
    ],
    "ASISTENTE": [lambda user: hasattr(user, "asistente"), lambda user: user.asistente],
    "ADMINISTRADOR": [
        lambda user: hasattr(user, "administrador"),
        lambda user: user.administrador,
    ],
    "DEVELOPER": [lambda user: hasattr(user, "developer"), lambda user: user.developer],
}

TABLA_ROL_OLD = {
    "PACIENTE": lambda user: hasattr(user, "paciente"),
    "DOCTOR": lambda user: hasattr(user, "doctor"),
    "ASISTENTE": lambda user: hasattr(user, "asistente"),
    "SUPERDOCTOR": lambda user: hasattr(user, "susperdoctor"),
    "ASISTENTE": lambda user: hasattr(user, "asistente"),
    "ADMINISTRADOR": lambda user: hasattr(user, "administrador"),
    "DEVELOPER": lambda user: hasattr(user, "developer"),
}


def GET_ROL(user):
    for rol, funcionList in TABLA_ROL.items():
        # lambda user tiene el atributo rol
        if funcionList[0](user):
            # lambda user devuelve el objeto rol
            return rol, funcionList[1](user)

    return "Sin rol", user


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
