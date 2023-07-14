from django.urls import path
from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView, CreateOrganizationsConnectionsAPI, OrganizationConnectionAPI


urlpatterns = [
    path('create', CreateOrganizationAPI.as_view(), name='organization-create'),
    
    path('employees', OrganizationEmployeeAPIView.as_view(), name='employee'),
    path('employees/<int:pk>', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),

    path('connection-create', CreateOrganizationsConnectionsAPI.as_view(), name='organization-connection-create'),
    path('connections/<int:id>', OrganizationConnectionAPI.as_view(), name='organization-connection'),
    
]
