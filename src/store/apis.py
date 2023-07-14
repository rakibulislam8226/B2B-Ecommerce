from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Products, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryCreateAPI(generics.CreateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] # Need to make custom permission and upgrade this


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Products.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated] # Need to make custom permission and upgrade this
