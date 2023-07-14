from django.contrib import admin
from .models import Organization, OrganizationEmployee, OrganizationConnection

# Register your models here.
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'website')


@admin.register(OrganizationEmployee)
class OrganizationEmployeeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'organization', 'role', 'is_default')
    search_fields = ( 'user__email', 'user__phone')
    list_filter = ('role',)


@admin.register(OrganizationConnection)
class OrganizationConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_organization', 'to_organization', 'connection_type')
    list_editable = ('connection_type',)