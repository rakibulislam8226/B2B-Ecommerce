from rest_framework import serializers
from .models import Organization, OrganizationEmployee, OrganizationConnection


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEmployee
        fields = "__all__"


class OrganizationConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationConnection
        fields = ('uid', 'created_at', 'updated_at', 'from_organization', 'to_organization', 'connection_type')  
