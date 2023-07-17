from rest_framework import serializers
from organizations.models import Organization
from .models import Products, Category, Cart, CartItem, Order, OrderItem
from organizations.models import Address
from django.contrib.auth import get_user_model

User = get_user_model()


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


class CartItemSerializer(serializers.ModelSerializer):
    cart = serializers.SlugRelatedField(slug_field='uid', queryset=Cart.objects.filter())
    product = serializers.SlugRelatedField(slug_field='uid', queryset=Products.objects.filter())
    
    class Meta:
        model = CartItem
        fields = ('uid', 'created_at', 'updated_at', 'cart', 'product', 'quantity')
        read_only_fields = ('uid', 'created_at', 'updated_at') 

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(slug_field='uid', queryset=User.objects.filter())

    class Meta:
        model = Cart
        fields = ('uid', 'created_at', 'updated_at', 'user', 'total_price', 'items')
        read_only_fields = ('uid', 'created_at', 'updated_at', 'total_price') 

    def get_total_price(self, obj):
        return obj.total_price


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='uid', queryset=User.objects.filter())

    class Meta:
        model = Order
        fields = ['uid', 'user', 'total_price', 'shipping_address', 'created_at', 'updated_at']
        read_only_fields = ['uid', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='uid', queryset=Products.objects.filter())
    order = serializers.SlugRelatedField(slug_field='uid', queryset=Order.objects.filter())

    class Meta:
        model = OrderItem
        fields = ['uid', 'created_at', 'updated_at', 'order', 'product', 'quantity', 'unit_price']
        read_only_fields = ['uid', 'created_at', 'updated_at']