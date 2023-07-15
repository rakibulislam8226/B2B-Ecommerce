from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView, CreateOrganizationsConnectionsAPI, \
                    OrganizationConnectionAPI, AddressListAPI, AddressDetailAPI


urlpatterns = [
    path('addresses', AddressListAPI.as_view(), name='address-list'),
    path('addresses/<str:uid>', AddressDetailAPI.as_view(), name='address-detail'),
    
    path('create', CreateOrganizationAPI.as_view(), name='organization-create'),
    
    path('employees', OrganizationEmployeeAPIView.as_view(), name='employee'),
    path('employees/<int:pk>', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),

    path('connection-create', CreateOrganizationsConnectionsAPI.as_view(), name='organization-connection-create'),
    path('connections/<int:id>', OrganizationConnectionAPI.as_view(), name='organization-connection'),
    
]
