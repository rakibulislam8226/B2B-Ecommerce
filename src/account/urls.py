from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .api import RegisterUserAPIView, LoginAPI, LogoutAPI
from .views import LogoutAPIView


urlpatterns = [
    path("register", RegisterUserAPIView.as_view(), name="user-register"),
    path("login", LoginAPI.as_view(), name="login"),
    path("logout", LogoutAPI.as_view(), name="logout"),
    # path('logout/v1', LogoutAPIView.as_view(), name='logoutv1'), # Using jwt token
    path("get-token", TokenObtainPairView.as_view(), name="get-token"),
    path("token-refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("token-verify", TokenVerifyView.as_view(), name="token-verify"),
]
