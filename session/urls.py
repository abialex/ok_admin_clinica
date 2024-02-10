from django.urls import path
# from session.views import signIn, signOut, check_session_and_authentication, createOrUpdateUserTokenFirebase
from rest_framework.authtoken import views

from session.routers import router
from session.views import AuthTokenLogin, AuthTokenDelete

app_name = 'session'

urlpatterns = [
    path("login", AuthTokenLogin.as_view()),
    path("logout", AuthTokenDelete.as_view()),
    #   path('signOut', signOut),
    #   path('autenticate', check_session_and_authentication),
    #   path('token-firebase', createOrUpdateUserTokenFirebase),
]

urlpatterns += router.urls
