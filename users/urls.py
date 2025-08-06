from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import ChangePasswordView, MeAPIView, RegisterAPIView

app_name = UsersConfig.name

urlpatterns = [
    # token
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # user
    path("register/", RegisterAPIView.as_view(), name="user-register"),
    path("me/", MeAPIView.as_view(), name="user-me"),
    path("change-password/", ChangePasswordView.as_view(), name="user-change-password"),
]
