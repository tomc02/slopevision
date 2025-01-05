from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from rest_api.views import PlaceViewSet, WebcamViewSet, WebcamHistoryViewSet, CustomUserDetailsView

# Create the router
router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'webcams', WebcamViewSet)
router.register(r'webcam-history', WebcamHistoryViewSet)

# Define the URLs
urlpatterns = [path('admin/', admin.site.urls), path('api/', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Generates the OpenAPI schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),  # Swagger UI
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration endpoints
    path('api/auth/user/', CustomUserDetailsView.as_view(), name='user-details'),
    path('api/auth/', include('dj_rest_auth.urls')),  # Authentication endpoints
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
