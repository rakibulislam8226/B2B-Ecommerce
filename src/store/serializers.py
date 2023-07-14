from rest_framework import serializers
from organizations.models import Organization
from .models import Products, Category

class ProductSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(slug_field='uid', queryset=Organization.objects.all())
    category = serializers.SlugRelatedField(slug_field='uid', queryset=Category.objects.all())

    class Meta:
        model = Products
        fields = ['product_name', 'organization', 'category', 'price', 'quantity', 'description']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']