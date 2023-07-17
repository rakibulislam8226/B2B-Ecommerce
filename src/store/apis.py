import uuid
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.db.models import Q

from .models import Products, Category, Cart, CartItem, Order
from organizations.models import OrganizationConnection, OrganizationEmployee, Organization, Address
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer, OrderSerializer
from .custom_permissions import IsInOrganization, IsOrganizationAdminOrOwner, IsUserCartOwner


class CategoryCreateAPI(generics.CreateAPIView):
    queryset = Category.objects.filter()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated] # Need to make custom permission and upgrade this


class ProductCreateAPI(generics.CreateAPIView):
    queryset = Products.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = [IsOrganizationAdminOrOwner]


class ProductListAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsInOrganization] # Not necessary to Custom permission that only organizations employee can see.

    def get_queryset(self):
        user = self.request.user
        organization_ids = user.organization_employee.filter(is_default=True).values_list('organization__id', flat=True).distinct()
        
        # Get organizations id with accepted status
        connected_organization_ids = OrganizationConnection.objects.filter(
            Q(from_organization__in=organization_ids) | Q(to_organization__in=organization_ids),
            connection_type='Accepted'
        ).values_list('from_organization', 'to_organization')

        organization_ids = set(organization_ids).union(*connected_organization_ids) # marge the organization ids with user organizations ids
        return Products.objects.filter(organization_id__in=organization_ids)


class CartCreateAPI(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if Cart.objects.filter(user=user).exists():
            raise APIException("A cart already exists for this user.")

        try:
            serializer.save(user=user, uid=uuid.uuid4())
        except Exception as e:
            raise APIException("Failed to create the cart. Please try again.")



class CartItemCreateAPI(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsUserCartOwner]
    # TODO: insert items in carts by user carts auto detect.


class CartListAPI(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsUserCartOwner]

    def get_queryset(self):
        """ Authenticated user can see his own carts details only. """
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            return Response({"message": "Your cart is empty"}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.filter()
    serializer_class = CartItemSerializer
    lookup_field = 'uid'

    def destroy(self, request, *args, **kwargs):
        """Just for show deleted response"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Cart item deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CheckoutAPI(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Employee shipping address
        try:
            organization_employee = user.organization_employee.first()
            shipping_address = organization_employee.organization.address
        except OrganizationEmployee.DoesNotExist:
            return Response({"error": "User is not associated with any organization."}, status=status.HTTP_400_BAD_REQUEST)
        except Organization.DoesNotExist:
            return Response({"error": "Organization not found."}, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"error": "Shipping address not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            shipping_address=shipping_address
        )
        order.items.set(cart_items)
        cart_items.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


