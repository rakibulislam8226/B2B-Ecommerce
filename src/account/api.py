from datetime import timedelta
from django.utils import timezone
from axes.models import AccessAttempt

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .serializers import (
    UserSerializer,
    LoginSerializer,
    LogoutTestSerializer,
    RegisterUserSerializers,
)

User = get_user_model()


class RegisterUserAPIView(APIView):
    serializer_class = RegisterUserSerializers

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        response_data = {"user": serializer.data, "token": token}
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    """
    Login api with axes and some custom limitations.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        password = serializer.validated_data["password"]

        # Get the client IP address from the request's META dictionary
        ip_address = request.META.get("REMOTE_ADDR")

        # Check if user is already locked out
        user_locked_out = AccessAttempt.objects.filter(
            username=phone, ip_address=ip_address, failures_since_start__gte=3
        ).first()

        if user_locked_out:
            if user_locked_out.failures_since_start >= 3:
                if (
                    user_locked_out.attempt_time + timedelta(minutes=15)
                    > timezone.now()
                ):
                    remaining_time = (
                        user_locked_out.attempt_time
                        + timedelta(minutes=15)
                        - timezone.now()
                    )
                    return Response(
                        {
                            "error": f"Account temporarily blocked. Please try again after {remaining_time.total_seconds()//60} minutes."
                        }
                    )
                else:
                    """Reset failed login attempts since the cooldown period is over"""
                    user_locked_out.failures_since_start = 0
                    user_locked_out.save()

        user = authenticate(request=request, username=phone, password=password)

        if user is not None:
            AccessAttempt.objects.filter(username=phone, ip_address=ip_address).delete()

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            token, created = Token.objects.get_or_create(
                user=user
            )  # NOTE: Token is use just for testing. it not necessary.

            response_data = {
                "refresh_token": str(refresh),
                "access_token": str(access),
                "token": (token.key),  # For testing
            }
            return Response(response_data)
        else:
            """Create or update failed login attempt record"""
            attempt, created = AccessAttempt.objects.get_or_create(
                username=phone, ip_address=ip_address
            )
            attempt.failures_since_start += 1
            attempt.attempt_time = timezone.now()
            attempt.save()

            return Response({"error": "Invalid credentials"})


class LogoutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutTestSerializer

    def post(self, request):
        # Simply delete the token to force a user to authenticate again
        request.user.auth_token.delete()
        return Response({"message": "Logout successful"})
