from django.urls import path
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView, CreateOrganizationsConnectionsAPI, \
                    OrganizationConnectionAPI, AddressListAPI, AddressDetailAPI


urlpatterns = [
    path('/addresses', AddressListAPI.as_view(), name='address-list'),
    path('/address/<str:uid>', AddressDetailAPI.as_view(), name='address-detail'),
    
    path('', CreateOrganizationAPI.as_view(), name='organization-create'),
    
    path('/employees', OrganizationEmployeeAPIView.as_view(), name='employee'),
    path('/employee/<int:pk>', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),

    path('/connections', CreateOrganizationsConnectionsAPI.as_view(), name='organization-connection-create'),
    path('/connection/<int:pk>', OrganizationConnectionAPI.as_view(), name='organization-connection'),
    
]
