from django.urls import path
from .apis import ProductCreateAPI, CategoryCreateAPI


urlpatterns = [
    path('category/create', CategoryCreateAPI.as_view(), name='category-create'),
    path('products/create', ProductCreateAPI.as_view(), name='product-create'),
]
