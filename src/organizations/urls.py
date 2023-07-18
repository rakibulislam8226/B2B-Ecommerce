from django.urls import path

from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView, CreateOrganizationsConnectionsAPI, \
                    OrganizationConnectionAPI, AddressListAPI, AddressDetailAPI, OrganizationDetailAPI


urlpatterns = [
    
    path('/connections/<int:pk>', OrganizationConnectionAPI.as_view(), name='organization-connection'),
    path('/connections', CreateOrganizationsConnectionsAPI.as_view(), name='organization-connection-create'),
    
    path('/employees/<int:pk>', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),
    path('/employees', OrganizationEmployeeAPIView.as_view(), name='employee'),
    
    path('/addresses/<str:uid>', AddressDetailAPI.as_view(), name='address-detail'),
    path('/addresses', AddressListAPI.as_view(), name='address-list'),
    
    path('/<str:uid>', OrganizationDetailAPI.as_view(), name='organization-detail'),
    path('', CreateOrganizationAPI.as_view(), name='organization-create'),
    
]
