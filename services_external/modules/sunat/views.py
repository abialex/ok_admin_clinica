from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from services_external.models import AccessToken, TokenFirebase
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from services_external.modules.firebase.serializers import TokenFirebaseSerializer
from shared.utils.Global import ERROR_MESSAGE, STRING, SUCCESS_MESSAGE
from shared.utils.decoradores import validar_data_serializer
import requests


@api_view(("GET",))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPersonaSunByDni(request, dni):
    result = apiRequestSunat(dni)

    if result.status_code == 200:
        personSun = result.json()
        data = SUCCESS_MESSAGE(
            tipo="list",
            message=result.reason,
            data=personSun,
            url=request.get_full_path(),
        )
        return Response(data, status=status.HTTP_200_OK)
    elif result.status_code == 401:
        data = ERROR_MESSAGE(
            tipo="error",
            message=result.reason,
            fields_errors={},
            url=request.get_full_path(),
        )
        return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        data = ERROR_MESSAGE(
            tipo=result.status_code.__str__(),
            message=result.reason,
            fields_errors={},
            url=request.get_full_path(),
        )
    return Response(data, status=status.HTTP_404_NOT_FOUND)


def apiRequestSunat(dni):
    myToken = AccessToken.objects.get(service="SUNAT")

    try:
        headers = {"Authorization": f"Bearer {myToken.token}"}
        response = requests.get(
            f"https://api.apis.net.pe/v2/reniec/dni?numero={dni}", headers=headers
        )
        return response

    except Exception as e:
        print(e.__str__())
        return None
