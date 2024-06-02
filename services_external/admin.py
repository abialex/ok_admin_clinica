from django.contrib import admin

from services_external.models import TokenFirebase, AccessToken

# Register your models here.
admin.site.register(TokenFirebase)
admin.site.register(AccessToken)
