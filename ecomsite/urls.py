from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/schema', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/v1/docs', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('organization.urls')),
    path('api/v1/', include('product.urls')),
    path('api/v1/', include('cart.urls')),
] + debug_toolbar_urls()

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
