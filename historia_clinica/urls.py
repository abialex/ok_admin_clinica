from historia_clinica.routers import router
app_name = 'historia_clinica'
urlpatterns = [


#    path('historia_clinica/', CitasViewSet.as_view(), name='historia_clinica'),
   # path('autenticate', check_session_and_authentication),
   # path('token-firebase', createOrUpdateUserTokenFirebase),
]

urlpatterns += router.urls