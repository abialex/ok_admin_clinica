from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from services_external.models import TokenFirebase
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from services_external.modules.firebase.serializers import TokenFirebaseSerializer
from shared.utils.Global import STRING
from shared.utils.decoradores import validar_data_serializer


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
    return token.id, "creado" if created else "modificado"
