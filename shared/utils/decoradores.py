from shared.utils.Global import ERROR_MESSAGE, SUCCESS_MESSAGE
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnDict


def validar_serializer(serializer):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            # obteniendo el request
            request = next(filter(lambda x: type(x) == Request, args), None)
            result_serializer = serializer(data=request.data)
            if result_serializer.is_valid():
                # agregando el nuevo argumento
                args = args + (result_serializer.data,)
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


def validar_data_serializer(from_dict, serializer):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            # obteniendo el request
            request = next(filter(lambda x: type(x) == Request, args), None)
            result_serializer = serializer(data=request.data)
            if result_serializer.is_valid():
                model = from_dict(result_serializer.data)
                # agregando el nuevo argumento
                args = args + (model,)

                data, crudString = funcion(*args, **kwargs)
                custom_response_data = SUCCESS_MESSAGE(
                    tipo=type(model).__name__,
                    message=type(model).__name__ + " " + crudString,
                    url=request.get_full_path(),
                    data=data,
                )
                return Response(
                    custom_response_data,
                    status=(
                        status.HTTP_201_CREATED
                        if crudString == "creado"
                        else status.HTTP_200_OK
                    ),
                )

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

            # agregando el nuevo argumento
            return funcion(*args, **kwargs)

        return wrapper

    return decorador
