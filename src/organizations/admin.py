from django.contrib import admin
from .models import Address, Organization, OrganizationEmployee, OrganizationConnection

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('house_no', 'village', 'post_office', 'thana', 'district')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')


@admin.register(OrganizationEmployee)
class OrganizationEmployeeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'organization', 'role', 'is_default')
    search_fields = ( 'user__email', 'user__phone')
    list_filter = ('role',)


@admin.register(OrganizationConnection)
class OrganizationConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_organization', 'to_organization', 'connection_type')
    list_editable = ('connection_type',)