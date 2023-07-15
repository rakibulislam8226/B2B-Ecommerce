from django.urls import path
from .apis import ProductCreateAPI, CategoryCreateAPI, ProductListAPI, CartListAPI, CartCreateAPI, \
    CartItemCreateAPI, CartItemUpdateDeleteAPI


urlpatterns = [
    path('category/create', CategoryCreateAPI.as_view(), name='category-create'),
    path('products/create', ProductCreateAPI.as_view(), name='product-create'),
    path('products/list', ProductListAPI.as_view(), name='product-list'),

    path('carts/create', CartCreateAPI.as_view(), name='cart-create'),
    path('carts/items/create', CartItemCreateAPI.as_view(), name='cart-items-create'),
    path('carts', CartListAPI.as_view(), name='cart-list'),
    # path('cart-items/<uuid:uid>', CartItemUpdateAPI.as_view(), name='cart-item-update'),
    # path('cart-items/<uuid:uid>', CartItemDeleteAPI.as_view(), name='cart-item-delete'),
    path('cart-items/<uuid:uid>/', CartItemUpdateDeleteAPI.as_view(), name='cart-item-update-delete'),
]
