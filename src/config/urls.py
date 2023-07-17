from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView, SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),
    path('we', include('organizations.urls')),
    path('we', include('store.urls')),

    path('api-auth/', include('rest_framework.urls')),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

admin.site.site_header = settings.APP_SITE_HEADER
admin.site.site_title = settings.APP_SITE_TITLE
admin.site.index_title = settings.APP_INDEX_TITLE