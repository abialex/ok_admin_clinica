from django.urls import path
#from session.views import signIn, signOut, check_session_and_authentication, createOrUpdateUserTokenFirebase
from rest_framework.authtoken import views

from session.routers import router

app_name = 'session'

urlpatterns = [

    path('generate_token', views.obtain_auth_token),
 #   path('signOut', signOut),
 #   path('autenticate', check_session_and_authentication),
 #   path('token-firebase', createOrUpdateUserTokenFirebase),
]

urlpatterns += router.urls
