import json
import traceback
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from shared.utils.Global import ERROR_MESSAGE, LOGGING_SAVE


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "El recurso no fue encontrado."

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail


def custom_exception_handler(exc, context):
    try:
        exception_class = exc.__class__.__name__
        handlers = {
            "InvalidToken": {"token": "An authorization token is not valid."},
            "ValidationError": _handler_validation_error,
            # Add more handlers as needed
        }
        res = exception_handler(exc, context)

        if "ValidationError" == exception_class:
            message = "Estos campos no están validados"
            fields_errors = handlers[exception_class](exc, context, res)
        elif "AuthenticationFailed" == exception_class:
            message = "La sesión expiró"
            fields_errors = {exception_class: str(exc)}
        elif "Http404" == exception_class:
            message = "No encontrado"
            fields_errors = {exception_class: str(exc)}
        elif "MethodNotAllowed" == exception_class:
            message = "Método no soportado"
            fields_errors = {exception_class: str(exc)}
        elif "NotAuthenticated" == exception_class:
            message = "No se proporcionaron las credenciales de autenticación"
            fields_errors = {exception_class: str(exc)}
        elif "IntegrityError" == exception_class:
            message = geIntegrytyErrorCustom(str(exc))
            fields_errors = {exception_class: str(exc)}
        else:
            # error no especificado
            message = "problema no definido"
            fields_errors = {exception_class: str(exc)}
        LOGGING_SAVE(exc=exc, url=context["request"].path)

        return Response(
            data=ERROR_MESSAGE(
                tipo=exception_class,
                message=message,
                fields_errors=fields_errors,
                url=context["request"].path,
            ),
            status=500 if res == None else res.status_code,
        )
    except Exception as e:
        LOGGING_SAVE(exc=e, url=context["request"].path)
        return Response(
            data=ERROR_MESSAGE(
                tipo=e.__str__(),
                message="Problema en el control de errores",
                fields_errors={},
                url=context["request"].path,
            ),
            status=500,
        )


def _handler_validation_error(exc, context, response):
    formatted_errors = {}
    if vars(exc).get("detail"):
        for field, errors in exc.detail.items():
            # Asumiendo que siempre quieres el primer mensaje de error
            formatted_errors[field] = errors[0] if errors else "Error desconocido"
        return formatted_errors
    return {"general": (exc.messages[0])}


@api_view(["GET", "POST", "DELETE", "UPDATE", "PUT"])
def custom_404(request, exception=None):
    response = ERROR_MESSAGE(
        tipo=type(request).__name__,
        message="la URL no existe",
        fields_errors={},
        url=request.path,
    )

    return Response(response, status=status.HTTP_404_NOT_FOUND)


def geIntegrytyErrorCustom(mensaje):
    match mensaje:
        case "UNIQUE constraint failed: recursos_humanos_doctor.dni":
            return "El DNI ya está registrado"
        case "02":
            return "February"
        case "03":
            return "March"
        case "04":
            return "April"
        case "05":
            return "May"
        case "06":
            return "June"
        case "07":
            return "July"
        case "08":
            return "August"
        case "09":
            return "September"
        case "10":
            return "October"
        case "11":
            return "November"
        case "12":
            return "December"
        case _:
            return "Una de las condiciones del sistema no se ha cumplido"
