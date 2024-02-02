from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    isNewPassword = models.BooleanField(default=True, verbose_name="¿Es nuevo usuario?")

    def __str__(self):
        return self.username


class UserTokenFirebase(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    username = models.CharField(max_length=10, unique=True, null=False)
    token = models.CharField(max_length=400, null=False)

    def __str__(self):
        return self.username
