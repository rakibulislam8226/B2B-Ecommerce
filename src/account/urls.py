from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .api import RegisterUserAPIView, LoginAPI, LogoutAPI


urlpatterns = [

    path('register/', RegisterUserAPIView.as_view(), name='user-register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout', LogoutAPI.as_view(), name='logout'),

    path('get-token/', TokenObtainPairView.as_view(), name='get-token'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token-verify'),
]