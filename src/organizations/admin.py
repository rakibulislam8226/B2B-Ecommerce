from django.contrib import admin
from .models import Address, Organization, OrganizationEmployee, OrganizationConnection

# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('uid', 'house_no', 'village', 'post_office', 'thana', 'district')
    readonly_fields =('uid',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'website')
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')


@admin.register(OrganizationEmployee)
class OrganizationEmployeeAdmin(admin.ModelAdmin):
    list_display = ('uid', 'slug', 'organization', 'role', 'is_default')
    list_editable = ('is_default',)
    search_fields = ( 'user__email', 'user__phone')
    list_filter = ('role',)
    readonly_fields = ("slug", 'created_at', 'updated_at', 'uid')


@admin.register(OrganizationConnection)
class OrganizationConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_organization', 'to_organization', 'connection_type')
    list_editable = ('connection_type',)
    readonly_fields = ('created_at', 'updated_at', 'uid')