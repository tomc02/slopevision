from django.contrib import admin

from rest_api.models import Place, Webcam, WebcamHistory, CustomUser

admin.site.register(Webcam)
admin.site.register(WebcamHistory)
admin.site.register(CustomUser)
admin.site.register(Place)
