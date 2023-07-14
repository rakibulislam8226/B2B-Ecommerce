from rest_framework import serializers
from store.models import Category
from .models import Organization, OrganizationEmployee, OrganizationConnection, Address


class OrganizationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='uid', queryset=Category.objects.filter())
    class Meta:
        model = Organization
        fields = ('uid', 'created_at', 'updated_at', 'name', 'slug', 'address', 'category', 'website')
        read_only_fields = ('uid', 'created_at', 'updated_at')


class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEmployee
        fields = "__all__"


class OrganizationConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationConnection
        fields = ('uid', 'created_at', 'updated_at', 'from_organization', 'to_organization', 'connection_type')  
