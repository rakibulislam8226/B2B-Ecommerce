from django.contrib import admin
from .models import Category, Products, Cart, CartItem, Order, OrderItem

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'slug')
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')
    search_fields = ( 'name',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'organization', 'category', 'price')
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')
    search_fields = ( 'name',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('uid', 'user',)
    readonly_fields = ('created_at', 'updated_at', 'uid')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('uid', 'cart', 'product', 'quantity')
    readonly_fields = ('created_at', 'updated_at', 'uid')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('uid', 'created_at', 'updated_at', 'user', 'total_price', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at', 'uid')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('uid', 'created_at', 'updated_at', 'order', 'product', 'quantity', 'unit_price')
    readonly_fields = ('created_at', 'updated_at', 'uid')




