from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import OrganizationEmployee, OrganizationConnection, Address, Organization
from .serializers import (
    OrganizationSerializer,
    OrganizationEmployeeSerializer,
    OrganizationConnectionSerializer,
    AddressSerializer,
    OrganizationsEmployeeTestSerialiser,
)

from store.custom_permissions import (
    IsOrganizationAdminOrOwner,
    OrganizationsConnectionStatusChangePermission,
)


class AddressListAPI(generics.ListCreateAPIView):
    queryset = Address.objects.filter()
    serializer_class = AddressSerializer


class AddressDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.filter()
    serializer_class = AddressSerializer
    lookup_field = "uid"


class CreateOrganizationAPI(generics.ListCreateAPIView):
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.filter()
    serializer_class = OrganizationSerializer
    lookup_field = "uid"


# FIXME: here is an problems while getting one specific elements. need to fix.
class OrganizationEmployeeAPIView(APIView):
    serializer_class = OrganizationsEmployeeTestSerialiser  # NOTE: Just for skipping the warning in terminal which i got during swagger load

    """Organizations Employees all api"""

    permission_classes = [IsOrganizationAdminOrOwner]

    def get(self, request, pk=None):
        if pk is not None:
            try:
                organization_employee = request.user.organization_employee.get(pk=pk)
                serializer = OrganizationEmployeeSerializer(organization_employee)
                return Response(serializer.data)
            except OrganizationEmployee.DoesNotExist:
                return Response(
                    {"error": "Organization's employee not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        organization_employees = (
            OrganizationEmployee.objects.filter()
        )  # TODO: if needed then get request user organization id and filter it.
        serializer = OrganizationEmployeeSerializer(organization_employees, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = OrganizationEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization_employee_data = serializer.validated_data

        organization = organization_employee_data["organization"]
        user = organization_employee_data["user"][0].id  # TODO: use first()

        if OrganizationEmployee.objects.filter(
            organization=organization, user=user
        ).exists():
            raise ValidationError("Employee already present this organization.")

        organization_employee = serializer.save()
        serialized_employee = OrganizationEmployeeSerializer(organization_employee)
        return Response(serialized_employee.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        try:
            organization_employees = OrganizationEmployee.objects.get(pk=pk)
        except OrganizationEmployee.DoesNotExist:
            return Response(
                {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )  # direct not found

        serializer = OrganizationEmployeeSerializer(
            organization_employees, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        organization_employees = serializer.save()
        return Response(OrganizationEmployeeSerializer(organization_employees).data)

    def delete(self, request, pk):
        try:
            organization_employees = OrganizationEmployee.objects.get(pk=pk)
        except OrganizationEmployee.DoesNotExist:
            return Response(
                {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )

        organization_employees.delete()
        return Response(
            {"success": "Employee delete successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CreateOrganizationsConnectionsAPI(generics.CreateAPIView):
    """Organizations connections create"""

    serializer_class = OrganizationConnectionSerializer
    permission_classes = [OrganizationsConnectionStatusChangePermission]


class OrganizationConnectionAPI(generics.RetrieveUpdateAPIView):
    queryset = OrganizationConnection.objects.filter()
    serializer_class = OrganizationConnectionSerializer
    permission_classes = [OrganizationsConnectionStatusChangePermission]
    lookup_field = "pk"
