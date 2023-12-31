import uuid
from autoslug import AutoSlugField

from django.db import models
from django.contrib.auth import get_user_model

from .choices import EMPLOYEE_ROLE, CONNECTION_STATUS

from config.models.TimeStampMixin import TimeStampMixin
from store.models import Category

# Create your models here.
User = get_user_model()


class Address(TimeStampMixin):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    house_no = models.CharField(max_length=30)
    village = models.CharField(max_length=100)
    post_office = models.CharField(max_length=10)
    thana = models.CharField(max_length=50)
    district = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.house_no}"

    @property
    def address(self):
        return f"{self.house_no}, {self.village}, {self.post_office}, {self.thana}, {self.district}"


class Organization(TimeStampMixin):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=("name"), max_length=255, editable=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    website = models.URLField(help_text="www.example.com", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "Organization"
        ordering = ("-id",)


class OrganizationEmployee(TimeStampMixin):
    """Employee of an organizations based on roles"""

    user = models.ManyToManyField(
        User,
        related_name="organization_employee",
        help_text="It is employee of the comapny.",
    )
    slug = AutoSlugField(populate_from=("role"), max_length=255, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)
    role = models.CharField(max_length=255, choices=EMPLOYEE_ROLE, default="Customer")
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.slug}"

    class Meta:
        verbose_name = "Organizations Employee"
        ordering = ("-id",)


class OrganizationConnection(TimeStampMixin):
    from_organization = models.ForeignKey(
        Organization, on_delete=models.RESTRICT, related_name="from_organization"
    )  # change name
    to_organization = models.ForeignKey(
        Organization, on_delete=models.RESTRICT, related_name="to_organization"
    )
    connection_type = models.CharField(
        max_length=255, choices=CONNECTION_STATUS, default="Pending"
    )

    def __str__(self) -> str:
        return f"{self.from_organization} -- {self.to_organization}"

    class Meta:
        verbose_name = "Organizations Connection"
        ordering = ("-id",)
