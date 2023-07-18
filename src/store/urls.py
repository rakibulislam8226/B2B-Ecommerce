from django.urls import path
from .apis import ProductCreateAPI, CategoryCreateAPI, ProductListAPI, CartListAPI, CartCreateAPI, \
    CartItemCreateAPI, CartItemUpdateDeleteAPI, CheckoutAPI, OrderAPI, OrderDetailAPI, OrderItemsAPI, OrderItemsDetailAPI


urlpatterns = [
    path('/list/category', CategoryCreateAPI.as_view(), name='category-create'),

    path('/list/products', ProductCreateAPI.as_view(), name='product-create'),
    path('/detail/products', ProductListAPI.as_view(), name='product-list'),

    path('/list/carts', CartCreateAPI.as_view(), name='cart-create'),
    path('/list/carts/items', CartItemCreateAPI.as_view(), name='cart-items-create'),
    path('/list/carts', CartListAPI.as_view(), name='cart-list'),
    path('/detail/cart-items/<uuid:uid>', CartItemUpdateDeleteAPI.as_view(), name='cart-item-update-delete'),

    path('/list/orders', OrderAPI.as_view(), name='order-list'),
    path('/detail/orders/<int:pk>', OrderDetailAPI.as_view(), name='order-detail'),
    path('/list/orders-items', OrderItemsAPI.as_view(), name='order-items'),
    path('/detail/orders-items/<str:uid>', OrderItemsDetailAPI.as_view(), name='order-items-detail'),

    path('/list/checkout', CheckoutAPI.as_view(), name='checkout'),
]
