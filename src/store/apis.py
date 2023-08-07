import uuid

from django.db.models import Q, Sum

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException, NotFound

from .models import Products, Category, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from .custom_permissions import (
    IsInOrganization,
    IsOrganizationAdminOrOwner,
    IsUserCartOwner,
)

from organizations.models import (
    OrganizationConnection,
    OrganizationEmployee,
    Organization,
    Address,
)


class CategoryCreateAPI(generics.CreateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Products.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = [IsOrganizationAdminOrOwner]


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsInOrganization]

    def get_queryset(self):
        user = self.request.user
        organization_ids = (
            user.organization_employee.filter(is_default=True)
            .values_list("organization__id", flat=True)
            .distinct()
        )

        # Get organizations id with accepted status
        connected_organization_ids = OrganizationConnection.objects.filter(
            Q(from_organization__in=organization_ids)
            | Q(to_organization__in=organization_ids),
            connection_type="Accepted",
        ).values_list("from_organization", "to_organization")

        organization_ids = set(organization_ids).union(
            *connected_organization_ids
        )  # marge the organization ids with user organizations ids
        return Products.objects.filter(organization_id__in=organization_ids)


class CartCreateAPI(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    # check it
    def perform_create(self, serializer):
        user = self.request.user

        if Cart.objects.filter(user=user).exists():
            raise APIException(
                detail="A cart already exists for this user."
            )  # NotFound

        try:
            serializer.save(user=user, uid=uuid.uuid4())
        except Exception as e:
            raise APIException(detail="Failed to create the cart. Please try again.")


class CartItemCreateAPI(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsUserCartOwner]
    # TODO: insert items in carts by user carts auto detect.


class CartListAPI(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsUserCartOwner]

    def get_queryset(self):
        """Authenticated user can see his own carts details only."""
        user = self.request.user
        return Cart.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response(
                {"message": "Your cart is empty"}, status=status.HTTP_200_OK
            )  # 204 status.
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.filter()
    serializer_class = CartItemSerializer
    lookup_field = "uid"


class CheckoutAPI(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST
            )  # validation error dajngo ar.

        total_price = cart_items.aggregate(total=Sum("product__price"))["total"]

        if total_price is None:
            total_price = 0

        # Employee shipping address
        try:
            organization_employee = user.organization_employee.first()
            shipping_address = organization_employee.organization.address
        except OrganizationEmployee.DoesNotExist:
            raise NotFound(detail="User is not associated with any organization.")
        except Organization.DoesNotExist:
            raise NotFound(detail="Organization not found.")
        except Address.DoesNotExist:
            raise NotFound(detail="Shipping address not found.")

        # Create the order
        order = Order.objects.create(
            user=user, total_price=total_price, shipping_address=shipping_address
        )
        # TODO: Items is not saving yet
        order.items.set(cart_items)
        cart_items.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSpecificOrderMixin:
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderAPI(generics.ListCreateAPIView):
    # queryset = Order.objects.filter()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.filter()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderItemsAPI(generics.ListCreateAPIView):
    queryset = OrderItem.objects.filter()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class OrderItemsDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.filter()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uid"

    # def get_queryset(self):
    #     user = self.request.user
    #     return OrderItem.objects.filter(user=user)
