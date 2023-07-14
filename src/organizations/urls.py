from django.urls import path
from .apis import CreateOrganizationAPI, OrganizationEmployeeAPIView


urlpatterns = [
    path('create', CreateOrganizationAPI.as_view(), name='organization-create'),
    
    path('employees', OrganizationEmployeeAPIView.as_view(), name='employee-list'),
    path('employees/<int:pk>/', OrganizationEmployeeAPIView.as_view(), name='employee-detail'),
    
]
