from django.contrib import admin

from rest_api.models import Place, Webcam, WebcamHistory, CustomUser

# Register your models here.
admin.site.register(Place)
admin.site.register(Webcam)
admin.site.register(WebcamHistory)
admin.site.register(CustomUser)
