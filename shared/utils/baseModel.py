from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from session.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from threadlocals.threadlocals import get_current_user

class BaseModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Accede al usuario autenticado a través de request.user
        # Hace que se guarde automaticamente el USER
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Accede al usuario autenticado a través de request.user
        # Hace que se guarde automaticamente el USER
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by', null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
