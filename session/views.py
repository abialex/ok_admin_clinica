import json

from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.sessions.models import Session
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import exception_handler

#from core.models import UserRol, UserSede
#from core.serializers import UserRolSerializer, UserSedeSerializer
from session.models import UserTokenFirebase
from session.serializers import *
#from Utils import create_response_succes, create_response_error

