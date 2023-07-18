from rest_framework import serializers
from store.models import Category
from django.contrib.auth import get_user_model
from .models import Organization, OrganizationEmployee, OrganizationConnection, Address
from account.serializers import UserSerializer

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    class Meta:
        model = Address
        fields = ('uid', 'house_no', 'village', 'post_office', 'thana', 'district', 'address')
        read_only_fields = ('uid', 'address')

    def address(self, obj)  -> str:
        return obj.address


class OrganizationSerializer(serializers.ModelSerializer):
    address = serializers.SlugRelatedField(slug_field='uid', queryset=Address.objects.filter())
    category = serializers.SlugRelatedField(slug_field='uid', queryset=Category.objects.filter())

    class Meta:
        model = Organization
        fields = ('uid', 'created_at', 'updated_at', 'name', 'slug', 'address', 'category', 'website')
        read_only_fields = ('uid', 'created_at', 'updated_at')


class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(slug_field='uid', queryset=Organization.objects.filter())
    #FIXME: user fields not working according to expectations because of many_to_many field.
    # user = serializers.SlugRelatedField(slug_field='uid', queryset=User.objects.filter())

    class Meta:
        model = OrganizationEmployee
        fields = ('uid', 'created_at', 'updated_at', 'user', 'slug', 'organization', 'role', 'is_default')
        read_only_fields = ('uid', 'created_at', 'updated_at')

        
class OrganizationsEmployeeTestSerialiser(serializers.Serializer):
    pass


class OrganizationConnectionSerializer(serializers.ModelSerializer):
    from_organization = serializers.SlugRelatedField(slug_field='uid', queryset=Organization.objects.filter())
    to_organization = serializers.SlugRelatedField(slug_field='uid', queryset=Organization.objects.filter())
    
    class Meta:
        model = OrganizationConnection
        fields = ('uid', 'created_at', 'updated_at', 'from_organization', 'to_organization', 'connection_type') 
        read_only_fields = ('uid', 'created_at', 'updated_at') 
