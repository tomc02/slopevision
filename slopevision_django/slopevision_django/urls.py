from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_api import views

from rest_api.views import PlaceViewSet, WebcamViewSet, WebcamHistoryViewSet
# Create the router
router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'webcams', WebcamViewSet)
router.register(r'webcam-history', WebcamHistoryViewSet)

# Define the URLs
urlpatterns = [path('admin/', admin.site.urls), path('api/', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # Generates the OpenAPI schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),  # Swagger UI
    re_path('login', views.login_view),
    re_path('registration', views.registration_view),
    re_path('user', views.user_view),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
