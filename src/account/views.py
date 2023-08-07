from rest_framework.response import Response
from rest_framework import status, generics, permissions

from .serializers import LogoutSerializer


# FIXME: Logout this api using access token or refresh token.
class LogoutAPIView(generics.GenericAPIView):
    """Create a logout api using access token"""

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
