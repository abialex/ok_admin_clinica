from django.forms import ValidationError
from rest_framework import serializers
from services_external.models import TokenFirebase
from session.models import User


class TokenFirebaseSerializer(serializers.Serializer):
    token_fcm = serializers.CharField()
    # usuario_id = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.filter(is_active=True),
    #     source="user",
    #     required=True,
    # )

    def validate_token_fcm(self, value):
        # Comprobar si el token_fcm ya existe
        if TokenFirebase.objects.filter(token_fcm=value).exists():
            raise ValidationError("El token FCM ya existe.")
        return value


class NotificationSerializer(serializers.Serializer):
    rol = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    body = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    data = serializers.JSONField(required=False, allow_null=True)
