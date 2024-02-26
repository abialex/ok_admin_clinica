from shared.utils.Global import ERROR_MESSAGE
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request


def validar_serializer(serializer):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            # obteniendo el request
            request = next(filter(lambda x: type(x) == Request, args), None)
            result_serializer = serializer(data=request.data)
            if result_serializer.is_valid():
                # agregando el nuevo argumento
                args = args + (result_serializer,)
                return funcion(*args, **kwargs)
            else:
                custom_response_data = ERROR_MESSAGE(
                    tipo="Validación",
                    message="Error de validación",
                    url=request.get_full_path(),
                    fields_errors=result_serializer.errors,
                )
                return Response(
                    custom_response_data, status=status.HTTP_400_BAD_REQUEST
                )

        return wrapper

    return decorador
