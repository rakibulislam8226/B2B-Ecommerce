from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import UserSerializer, LoginSerializer, LogoutTestSerializer, RegisterUserSerializers

User = get_user_model()

class RegisterUserAPIView(APIView):
    serializer_class = RegisterUserSerializers

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        response_data = {
            'user': serializer.data,
            'token': token
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']
        user = authenticate(phone=phone, password=password)

        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            token, created = Token.objects.get_or_create(user=user)

            # Create response data
            response_data = {
                'refresh_token': str(refresh),
                'access_token': str(access),
                'token': (token.key), # For testing
            }
            return Response(response_data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
       
        
class LogoutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutTestSerializer


    def post(self, request):
        # Simply delete the token to force a user to authenticate again
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'})