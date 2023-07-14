from django.db import models
from django.template.defaultfilters import slugify
from config.models.TimeStampMixin import TimeStampMixin
from django.contrib.auth import get_user_model
from .choices import EMPLOYEE_ROLE, CONNECTION_STATUS

# Create your models here.
User = get_user_model()


class Organization(TimeStampMixin):
    organization_name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    address = models.CharField(max_length=255)
    website = models.URLField(help_text='www.example.com', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.organization_name}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.organization_name)
        super(Organization, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Organization" 
        ordering = ('-id', )


class OrganizationEmployee(TimeStampMixin):
    """Employee of an organizations based on roles"""
    
    user = models.ManyToManyField(User, related_name = 'user', help_text='It is employee of the comapny.')
    slug = models.SlugField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)
    role = models.CharField(max_length=255, choices=EMPLOYEE_ROLE, default='Customer')
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.slug}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(f'{self.organization}-{self.role}')
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Organizations Employee" 
        ordering = ('-id', )
