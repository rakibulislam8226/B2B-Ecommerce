from django.contrib import admin
from .models import Organization, OrganizationEmployee

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'website')


@admin.register(OrganizationEmployee)
class OrganizationEmployeeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'organization', 'role', 'is_default')
    search_fields = ( 'user__email', 'user__phone')
    list_filter = ('role',)