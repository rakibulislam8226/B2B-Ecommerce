from django.db import models
import uuid


# This model will then not be used to create any database table.

class TimeStampMixin(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True