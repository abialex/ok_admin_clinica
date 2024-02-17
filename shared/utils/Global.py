import traceback

from shared.models import ErrorLog


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


TABLA_ROL = {
    "PACIENTE": lambda user: hasattr(user, "paciente"),
    "DOCTOR": lambda user: hasattr(user, "doctor"),
    "ASISTENTE": lambda user: hasattr(user, "asistente"),
    "SUPERDOCTOR": lambda user: hasattr(user, "susperdoctor"),
    "ASISTENTE": lambda user: hasattr(user, "asistente"),
    "ADMINISTRADOR": lambda user: hasattr(user, "administrador"),
    "DEVELOPER": lambda user: hasattr(user, "developer"),
}


def GET_ROL(user):
    for rol, check in TABLA_ROL.items():
        if check(user):
            return rol
    return "SIN ROL"


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
