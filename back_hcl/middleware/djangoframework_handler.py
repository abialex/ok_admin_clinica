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


from django.contrib import messages


def custom_exception_handler(exc, context):
    try:
        exception_class = exc.__class__.__name__
        handlers = {
            "Http404": {"Http404": "no se encontró el objeto."},
            "MethodNotAllowed": {"MethodNotAllowed": "método no soportado"},
            "AuthenticationFailed": {"token": "Token inválido."},
            "NotAuthenticated": {
                "authentication": "An authorization token is not provided."
            },
            "InvalidToken": {"token": "An authorization token is not valid."},
            "IntegrityError": {"integrityError": exc.__str__()},
            "ValidationError": _handler_validation_error,
            # Add more handlers as needed
        }
        res = exception_handler(exc, context)
        if "ValidationError" == exception_class:
            message = handlers[exception_class](exc, context, res)
        else:
            # error no especificado
            message = {exception_class: str(exc)}
        LOGGING_SAVE(exc=exc, url=context["request"].path)
        return Response(
            data=ERROR_MESSAGE(
                tipo=exception_class,
                message="Problemas en el backend",
                fields_errors=message,
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
