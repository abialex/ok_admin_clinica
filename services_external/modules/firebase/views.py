from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from cita.serializers import CitaSerializerByDateLocationDoctor
from services_external.models import TokenFirebase
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from services_external.modules.firebase.serializers import (
    NotificationSerializer,
    TokenFirebaseSerializer,
)
from services_external.modules.firebase.utils.firebase_config import Firebase
from shared.utils.Global import ERROR_MESSAGE, STRING, SUCCESS_MESSAGE
from shared.utils.decoradores import validar_data_serializer, validar_serializer
from firebase_admin import messaging


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_data_serializer(
    from_dict=TokenFirebase.from_dict, serializer=TokenFirebaseSerializer
)
def createOrUpdateUserTokenFirebase(
    request,
    cls: TokenFirebase,
):

    token, created = TokenFirebase.objects.get_or_create(usuario=request.user)
    if not created:
        token.token_fcm = cls.token_fcm
        token.save()
    return token.id, status.HTTP_201_CREATED if created else status.HTTP_200_OK


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@validar_serializer(serializer=NotificationSerializer)
def sendGroupNotification(request, data):
    rol = data["rol"]
    title = data["title"]
    body = data["body"]
    dataJson = data["data"]

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data=dataJson,
        topic=rol,
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)
    custom_response_data = SUCCESS_MESSAGE(
        tipo=type(int).__name__,
        message="token",
        url=request.get_full_path(),
        data={
            "mensaje": response,
            "isValid": "ss",
        },
    )

    return Response(custom_response_data, status=status.HTTP_200_OK)
