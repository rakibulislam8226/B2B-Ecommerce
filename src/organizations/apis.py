from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import OrganizationEmployee
from .serializers import OrganizationSerializer, OrganizationEmployeeSerializer



class CreateOrganizationAPI(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationEmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk=None):
        try:
            if pk:
                organization_employees = OrganizationEmployee.objects.get(pk=pk)
                serializer = OrganizationEmployeeSerializer(organization_employees)
                return Response(serializer.data)
        except OrganizationEmployee.DoesNotExist:
            return Response({"error": "Organization employee not found."}, status=status.HTTP_404_NOT_FOUND)

        organization_employees = OrganizationEmployee.objects.all()
        serializer = OrganizationEmployeeSerializer(organization_employees, many=True)
        return Response(serializer.data)
    
    #FIXME: If employee is already created in a organization then same employee can not be create again in same organizations.
    def post(self, request, pk=None):
        serializer = OrganizationEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            organization_employees = serializer.save()
            return Response(OrganizationEmployeeSerializer(organization_employees).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk, format=None):
        try:
            organization_employees = OrganizationEmployee.objects.get(pk=pk)
        except OrganizationEmployee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationEmployeeSerializer(organization_employees, data=request.data)
        if serializer.is_valid():
            organization_employees = serializer.save()
            return Response(OrganizationEmployeeSerializer(organization_employees).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        try:
            organization_employees = OrganizationEmployee.objects.get(pk=pk)
        except OrganizationEmployee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        organization_employees.delete()
        return Response({"success": "Employee delete successfully."}, status=status.HTTP_204_NO_CONTENT)
