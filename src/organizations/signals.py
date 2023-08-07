"""
Not yet use this. just define the signals for further purpose needed.
"""
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import OrganizationEmployee


@receiver(pre_save, sender=OrganizationEmployee)
def create_employee_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            f"{instance.user}-{instance.organization}-{instance.role}"
        )
