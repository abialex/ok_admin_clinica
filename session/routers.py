from rest_framework.routers import DefaultRouter
from session.views import UserViewSet

router = DefaultRouter()

router.register(r"user", UserViewSet, basename="user")
