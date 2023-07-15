from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import OrganizationEmployee, OrganizationConnection, Address
from store.custom_permissions import IsOrganizationAdminOrOwner
from .serializers import OrganizationSerializer, OrganizationEmployeeSerializer, OrganizationConnectionSerializer, \
                        AddressSerializer


class AddressListAPI(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'uid'

    def destroy(self, request, *args, **kwargs):
        """Just for show the confirmations the deleted response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Address deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CreateOrganizationAPI(generics.CreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationEmployeeAPIView(APIView):
    """Organizations Employees all api"""

    permission_classes = [IsOrganizationAdminOrOwner]

    def get(self, request, pk=None):
        if pk is not None:
            try:
                organization_employees = OrganizationEmployee.objects.get(pk=pk)
                serializer = OrganizationEmployeeSerializer(organization_employees)
                return Response(serializer.data)
            except OrganizationEmployee.DoesNotExist:
                return Response({"error": "Organization employee not found."}, status=status.HTTP_404_NOT_FOUND)
        #TODO: Override to get only own ogranizations employees list
        
        organization_employees = OrganizationEmployee.objects.filter()
        serializer = OrganizationEmployeeSerializer(organization_employees, many=True)
        return Response(serializer.data)
    
    #FIXME: If employee is already created in a organization then same employee can not be create again in same organizations.
    def post(self, request, pk=None):
        serializer = OrganizationEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_employees = serializer.save()
        return Response(OrganizationEmployeeSerializer(organization_employees).data, status=status.HTTP_201_CREATED)
    

    def put(self, request, pk, format=None):
        try:
            organization_employees = OrganizationEmployee.objects.get(pk=pk)
        except OrganizationEmployee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationEmployeeSerializer(organization_employees, data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_employees = serializer.save()
        return Response(OrganizationEmployeeSerializer(organization_employees).data)
    

    def delete(self, request, pk):
        try:
            organization_employees = OrganizationEmployee.objects.get(pk=pk)
        except OrganizationEmployee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        organization_employees.delete()
        return Response({"success": "Employee delete successfully."}, status=status.HTTP_204_NO_CONTENT)


class CreateOrganizationsConnectionsAPI(generics.CreateAPIView):

    #FIXME: the request will be auto detect by from_organization. only to_organizations have to set.
    serializer_class = OrganizationConnectionSerializer
    permission_classes = [IsOrganizationAdminOrOwner]


class OrganizationConnectionAPI(generics.RetrieveUpdateAPIView):
    queryset = OrganizationConnection.objects.filter()
    serializer_class = OrganizationConnectionSerializer
    permission_classes = [IsOrganizationAdminOrOwner]
    lookup_field = 'id' # Need id or uid?
