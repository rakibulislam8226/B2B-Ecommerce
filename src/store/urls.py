from django.urls import path

from .apis import (
    ProductCreateAPI,
    ProductListAPI,
    CartListAPI,
    CartCreateAPI,
    CartItemCreateAPI,
    CartItemUpdateDeleteAPI,
    CheckoutAPI,
    OrderAPI,
    OrderDetailAPI,
    OrderItemsAPI,
    OrderItemsDetailAPI,
)


urlpatterns = [
    path("/products/create", ProductCreateAPI.as_view(), name="product-create"),
    path("/products/lists", ProductListAPI.as_view(), name="product-list"),
    path("/carts/create", CartCreateAPI.as_view(), name="cart-create"),
    path("/carts/items", CartItemCreateAPI.as_view(), name="cart-items-create"),
    path("/carts/lists", CartListAPI.as_view(), name="cart-list"),
    path(
        "/carts/items/<uuid:uid>",
        CartItemUpdateDeleteAPI.as_view(),
        name="cart-item-update-delete",
    ),
    path("/orders/create", OrderAPI.as_view(), name="order-list"),
    path("/orders/<int:pk>", OrderDetailAPI.as_view(), name="order-detail"),
    path("/orders/items", OrderItemsAPI.as_view(), name="order-items"),
    path(
        "/orders/items/<str:uid>",
        OrderItemsDetailAPI.as_view(),
        name="order-items-detail",
    ),
    path("/checkout", CheckoutAPI.as_view(), name="checkout"),
]
