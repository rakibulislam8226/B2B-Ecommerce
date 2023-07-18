from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView, CreateOrganizationsConnectionsAPI, \
                    OrganizationConnectionAPI, AddressListAPI, AddressDetailAPI, OrganizationDetailAPI


urlpatterns = [
    
    path('/detail/connections/<int:pk>', OrganizationConnectionAPI.as_view(), name='organization-connection'),
    path('/list/connections', CreateOrganizationsConnectionsAPI.as_view(), name='organization-connection-create'),
    
    path('/detail/employees/<int:pk>', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),
    path('/list/employees', OrganizationEmployeeAPIView.as_view(), name='employee'),
    
    path('/detail/addresses/<str:uid>', AddressDetailAPI.as_view(), name='address-detail'),
    path('/list/addresses', AddressListAPI.as_view(), name='address-list'),
    
    path('/detail', OrganizationDetailAPI.as_view(), name='organization-detail'),
    path('/list', CreateOrganizationAPI.as_view(), name='organization-create'),
    
]
