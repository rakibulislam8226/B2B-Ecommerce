from django.urls import path
from .apis import ProductCreateAPI, CategoryCreateAPI, ProductListAPI


urlpatterns = [
    path('category/create', CategoryCreateAPI.as_view(), name='category-create'),
    path('products/create', ProductCreateAPI.as_view(), name='product-create'),
    path('products/list', ProductListAPI.as_view(), name='product-list'),
]
