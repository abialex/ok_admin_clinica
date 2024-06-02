from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from session.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from threadlocals.threadlocals import get_current_user
from django.contrib import admin


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

    def destroy(self, instance):
        instance.update_by = self.request.user
        instance.is_deleted = True
        instance.save()


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_created_by", null=True
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_updated_by", null=True
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseModelAdmin(admin.ModelAdmin):
    exclude = (
        "created_by",
        "updated_by",
        "notes",
    )  # Excluir estos campos del formulario de admin por defecto

    def save_model(self, request, obj, form, change):
        if (
            not obj.pk
        ):  # Si es una creación de objeto nuevo, pk (primary key) no estará establecida
            obj.created_by = request.user
        else:  # Si es una actualización, solo cambiamos 'updated_by'
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
