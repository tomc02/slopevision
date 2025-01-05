from django.contrib import admin

from rest_api.models import Place, Webcam, WebcamHistory, CustomUser
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = ('name', 'geolocation', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
admin.site.register(Webcam)
admin.site.register(WebcamHistory)
admin.site.register(CustomUser)
