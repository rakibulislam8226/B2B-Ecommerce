from rest_framework import serializers
from organizations.models import Organization
from .models import Products, Category

class ProductSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(slug_field='uid', queryset=Organization.objects.filter())
    category = serializers.SlugRelatedField(slug_field='uid', queryset=Category.objects.filter())

    class Meta:
        model = Products
        fields = ['uid', 'created_at', 'updated_at', 'name', 'organization', 'category', 'price', 'quantity', 'description']
        read_only_fields = ('uid', 'created_at', 'updated_at') 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['uid', 'created_at', 'updated_at', 'name', 'description']
        read_only_fields = ('uid', 'created_at', 'updated_at') 