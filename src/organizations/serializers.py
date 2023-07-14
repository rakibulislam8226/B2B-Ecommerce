from rest_framework import serializers
from .models import Organization, OrganizationEmployee


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class OrganizationEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationEmployee
        fields = "__all__"
