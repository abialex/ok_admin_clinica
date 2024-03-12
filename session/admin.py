from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from session.models import User


# Register your models here.
class CustomUserAdmins(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ("username", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("isNewPassword",)}),)


admin.site.register(User, CustomUserAdmins)
