from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Products, Category
from .serializers import ProductSerializer, CategorySerializer
from .custom_permissions import IsInOrganization, IsOrganizationAdminOrOwner


class CategoryCreateAPI(generics.CreateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] # Need to make custom permission and upgrade this


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Products.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = [IsOrganizationAdminOrOwner]


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsInOrganization] # Not necessary to Custom permission that only organizations employee can see.

    def get_queryset(self):
        user = self.request.user
        organization_ids = user.organization_employee.filter(is_default=True).values_list('organization__id', flat=True).distinct()
        return Products.objects.filter(organization_id__in=organization_ids)
