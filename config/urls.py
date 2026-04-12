from django.contrib import admin
from django.urls import path, include
from drf_yasg import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI interfeysi
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Redoc (muqobil interfeys)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
