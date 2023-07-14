from django.contrib import admin
from .models import Category, Products

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'uid', 'slug')
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')
    search_fields = ( 'name',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'category', 'price')
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')
    search_fields = ( 'name',)
