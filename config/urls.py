from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('insurance/', include('insurance.urls')),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]