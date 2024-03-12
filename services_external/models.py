from django.db import models

from session.models import User


# --------------------------------------------------TOKEN FIREBASE------------------------------------------------
class TokenFirebase(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    token_fcm = models.CharField(max_length=255, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    # Opcionalmente, podrías querer rastrear el tipo de dispositivo, sistema operativo, etc.
    tipo_dispositivo = models.CharField(max_length=100, blank=True, null=True)
    sistema_operativo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.usuario.username

    @classmethod
    def from_dict(cls, data):
        return cls(
            usuario_id=data.get("usuario_id", None),
            token_fcm=data.get("token_fcm", None),
            tipo_dispositivo=data.get("tipo_dispositivo", None),
            sistema_operativo=data.get("sistema_operativo", None),
        )


# ----------------------------------------------------------------------------------------------------------------
