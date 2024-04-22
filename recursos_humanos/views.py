from django.shortcuts import render

from session.models import User


# Create your views here.
def assignUsername(dni):
    contador = 2
    username = "slg_" + dni[:contador]
    while User.objects.filter(username=username).__len__() != 0:
        username = "slg_" + dni[:contador]
        contador += 1
    return username
