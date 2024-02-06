import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

from shared.utils.Global import error_message


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
            "Http404": _handler_Http404r,
            "MethodNotAllowed": _handler_MethodNotAllowed,
            "AuthenticationFailed": _handler_invalid_token,
            "NotAuthenticated": _handler_authentication_error,
            "InvalidToken": _handler_invalid_token_error,
            "ValidationError": _handler_validation_error,
            "IntegrityError": _integrityError_error,
            # Add more handlers as needed
        }
        res = exception_handler(exc, context)
        if exception_class in handlers:
            message = handlers[exception_class](exc, context, res)
        else:
            # if there is no hanlder is presnet
            message = str(exc)
        return Response(
            data=error_message(
                tipo=exception_class,
                message="Problemas en el backend",
                fields_errors=message,
                url=context["request"].path,
            ),
            status=500 if res == None else res.status_code,
        )
    except Exception as e:
        return Response(
            data=error_message(
                tipo=e.__str__(),
                message="Problema no detallado",
                fields_errors={},
                url=context["request"].path,
            ),
            status=500,
        )


def _handler_Http404r(exc, context, response):
    return {"Http404": ["no se encontró el objeto."]}


def _handler_authentication_error(exc, context, response):
    return {"authentication": ["An authorization token is not provided."]}


def _handler_MethodNotAllowed(exc, context, response):
    return {"MethodNotAllowed": ["método no soportado"]}


def _handler_invalid_token_error(exc, context, response):
    return {"token": ["An authorization token is not valid."]}


def _handler_invalid_token(exc, context, response):
    return {"token": ["Token inválido."]}


def _validation_error(exc, context, response):
    return {"token": ["Token inválido."]}


def _integrityError_error(exc, context, response):
    print(vars(exc))

    return {"integrityError": [exc.__str__()]}


def _handler_validation_error(exc, context, response):
    formatted_errors = {}
    if vars(exc).get("detail"):
        for field, errors in exc.detail.items():
            formatted_errors[field] = errors
            return formatted_errors
        return formatted_errors
    return exc.__str__()


@api_view(["GET", "POST", "DELETE", "UPDATE", "PUT"])
def custom_404(request, exception=None):
    response = error_message(
        tipo=type(request).__name__,
        message="No se encontró la URL",
        fields_errors={},
        url=request.path,
    )

    return Response(response, status=status.HTTP_404_NOT_FOUND)
