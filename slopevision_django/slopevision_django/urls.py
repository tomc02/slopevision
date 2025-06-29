from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from rest_api.views import PlaceViewSet, WebcamViewSet, WebcamHistoryViewSet, CustomUserDetailsView, get_csrf_token, AddFavoritePlaceView, RemoveFavoritePlaceView, FetchWebcamDataView, SaveHistoryView

# Create the router
router = DefaultRouter()
router.register(r'places', PlaceViewSet, basename='place')
router.register(r'webcams', WebcamViewSet)
router.register(r'webcam-history', WebcamHistoryViewSet)

# Define the URLs
urlpatterns = [path('admin/', admin.site.urls), path('api/', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Generates the OpenAPI schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),  # Swagger UI
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # Registration endpoints
    path('api/auth/user/', CustomUserDetailsView.as_view(), name='user-details'),
	path('api/auth/user/add-favorites/<int:place_id>/', AddFavoritePlaceView.as_view(), name='add-favorite'),
    path('api/auth/user/remove-favorites/<int:place_id>/', RemoveFavoritePlaceView.as_view(), name='remove-favorite'),
    path('api/auth/', include('dj_rest_auth.urls')),  # Authentication endpoints
    path('api/csrf/', get_csrf_token, name='get_csrf_token'),
    path('api/fetch-webcam-data/', FetchWebcamDataView.as_view(), name='fetch-webcam-data'),
    path('api/save-history/', SaveHistoryView.as_view(), name='save-history'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
