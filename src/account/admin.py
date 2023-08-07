from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone", "email", "is_active")
    list_editable = ("is_active",)
    search_fields = ("email", "phone")
    readonly_fields = ("id", "uid", "created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "uid",
                    "phone",
                    "email",
                    "password",
                    "last_login",
                    "groups",
                    "user_permissions",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
