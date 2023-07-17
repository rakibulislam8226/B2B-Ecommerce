from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView, CreateOrganizationsConnectionsAPI, \
                    OrganizationConnectionAPI, AddressListAPI, AddressDetailAPI


urlpatterns = [
    path('/list/addresses', AddressListAPI.as_view(), name='address-list'),
    path('/detail/addresses/<str:uid>', AddressDetailAPI.as_view(), name='address-detail'),
    
    path('', CreateOrganizationAPI.as_view(), name='organization-create'),
    
    path('/list/employees', OrganizationEmployeeAPIView.as_view(), name='employee'),
    path('/detail/employees/<int:pk>', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),

    path('/list/connections', CreateOrganizationsConnectionsAPI.as_view(), name='organization-connection-create'),
    path('/detail/connections/<int:pk>', OrganizationConnectionAPI.as_view(), name='organization-connection'),
    
]
