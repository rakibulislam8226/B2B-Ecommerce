from django.db import models
from config.models.TimeStampMixin import TimeStampMixin
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from store.models import Category
from .choices import EMPLOYEE_ROLE, CONNECTION_STATUS

# Create your models here.
User = get_user_model()

class Address(models.Model):
    house_no = models.CharField(max_length=30)
    village = models.CharField(max_length=100)
    post_office = models.CharField(max_length=10)
    thana = models.CharField(max_length=50)
    district = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.house_no}'


class Organization(TimeStampMixin):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=('name'), max_length=255, editable=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    website = models.URLField(help_text='www.example.com', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = "Organization" 
        ordering = ('-id', )


class OrganizationEmployee(TimeStampMixin):
    """Employee of an organizations based on roles"""
    
    user = models.ManyToManyField(User, related_name = 'user', help_text='It is employee of the comapny.')
    slug = AutoSlugField(populate_from=('user__email'), max_length=255, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)
    role = models.CharField(max_length=255, choices=EMPLOYEE_ROLE, default='Customer')
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.slug}'
    
    class Meta:
        verbose_name = "Organizations Employee" 
        ordering = ('-id', )


class OrganizationConnection(TimeStampMixin):

    from_organization = models.ForeignKey(Organization, on_delete=models.RESTRICT, related_name='from_organization')
    to_organization = models.ForeignKey(Organization, on_delete=models.RESTRICT, related_name='to_organization')
    connection_type = models.CharField(max_length=255, choices=CONNECTION_STATUS, default='Pending')

    def __str__(self) -> str:
        return f'{self.from_organization} -- {self.to_organization}'
    
    class Meta:
        verbose_name = "Organizations Connection" 
        ordering = ('-id', )
