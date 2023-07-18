from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from .models import Products


class IsInOrganization(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            organization_ids = user.organization_employee.filter(is_default=True).values_list('organization__id', flat=True).distinct()
            return Products.objects.filter(organization_id__in=organization_ids).exists()
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated and user.organization == obj.organization:
            return True
        return False


class IsOrganizationAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            organization_employee = user.organization_employee.filter(role__in=["Admin", "Owner"]).first()
            if organization_employee:
                organization_id = request.data.get("organization")
                user_organization_uid = str(organization_employee.organization.uid)
                if organization_id == user_organization_uid:
                    return True
        except Exception as e:
            raise PermissionDenied("Invalid permission")
        return False
    

class IsUserCartOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class OrganizationsConnectionStatusChangePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            organization_employee = user.organization_employee.filter(role__in=["Admin", "Owner"]).first()
            if organization_employee:
                return organization_employee.organization.uid
        except Exception as e:
            raise PermissionDenied("Invalid permission")
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            organization_employee = user.organization_employee.filter(role__in=["Admin", "Owner"]).first()
            if organization_employee:
                from_organization_uid = obj.from_organization.uid
                to_organization_uid = obj.to_organization.uid
                return (
                    organization_employee.organization.uid == from_organization_uid
                    or organization_employee.organization.uid == to_organization_uid
                )
        except Exception as e:
            raise PermissionDenied("Invalid permission")
        return False


    