from django.urls import path
from .apis import ProductCreateAPI, CategoryCreateAPI, ProductListAPI, CartListAPI, CartCreateAPI, \
    CartItemCreateAPI, CartItemUpdateDeleteAPI, CheckoutAPI


urlpatterns = [
    path('/category', CategoryCreateAPI.as_view(), name='category-create'),
    
    path('/product', ProductCreateAPI.as_view(), name='product-create'),
    path('/products', ProductListAPI.as_view(), name='product-list'),

    path('/cart', CartCreateAPI.as_view(), name='cart-create'),
    path('/cart/items', CartItemCreateAPI.as_view(), name='cart-items-create'),
    path('/carts', CartListAPI.as_view(), name='cart-list'),
    path('/cart-item/<uuid:uid>', CartItemUpdateDeleteAPI.as_view(), name='cart-item-update-delete'),

    path('/checkout', CheckoutAPI.as_view(), name='checkout'),
]
