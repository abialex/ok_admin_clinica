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
