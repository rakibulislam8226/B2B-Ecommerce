from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Products, Cart


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
                return True
                #FIXME: match employee organization id and request organization are same.
                # organization_id = request.data.get("organization_id")
                # # print(request.data.dict.organization)
                # print(request.__dict__['_data'].get("organization__id"))
                # print(organization_employee.organization_id)
                # if organization_id:
                #     return organization_employee.organization_id == organization_id
        except Exception as e:
            raise PermissionDenied("Invalid permission")
        return False
    

class IsUserCartOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    