from django.db import models
from django.contrib.auth import get_user_model

from config.models.TimeStampMixin import TimeStampMixin

from autoslug import AutoSlugField


User = get_user_model()


class Category(TimeStampMixin):
    name = models.CharField(max_length=255)  # will be unique?
    slug = AutoSlugField(populate_from="name", max_length=255, editable=False)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.slug}"

    class Meta:
        verbose_name = "Categories"
        ordering = ("-id",)


class Products(TimeStampMixin):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=("name"), max_length=255, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.slug}"

    class Meta:
        verbose_name = "Products"
        ordering = ("-id",)


class Cart(TimeStampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = "Cart"
        ordering = ("-id",)


class CartItem(TimeStampMixin):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product}"

    class Meta:
        verbose_name = "CartItem"
        ordering = ("-id",)


class Order(TimeStampMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.JSONField(default=dict)

    def __str__(self):
        return f"Order #{self.pk}  -- {self.user}"


class OrderItem(TimeStampMixin):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    product = models.ForeignKey(Products, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.pk}  -- {self.order}"
