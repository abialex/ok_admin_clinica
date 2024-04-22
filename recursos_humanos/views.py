from django.shortcuts import render

from session.models import User


# Create your views here.
def assignUsername(dni, prefix):
    contador = 2
    username = prefix + dni[:contador]
    while User.objects.filter(username=username).__len__() != 0:
        username = prefix + dni[:contador]
        contador += 1
    return username
