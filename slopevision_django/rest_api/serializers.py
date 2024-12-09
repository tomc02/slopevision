from rest_framework import serializers
from .models import Place, Webcam, WebcamHistory

class PlaceSerializer(serializers.ModelSerializer):
    # Nested serializer for webcams (weather data and forecasts have been removed as per your instruction)
    webcams = serializers.StringRelatedField(many=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'geolocation', 'description', 'webcams']


class WebcamSerializer(serializers.ModelSerializer):
    # If source_url is not provided, provide a link to the image instead (as url field)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Webcam
        fields = ['id', 'place', 'name', 'url', 'source_type', 'source_url', 'page_url', 'img_page_url', 'img_tag_id', 'last_updated', 'history_rate']

    def get_url(self, obj):
        # If source_url is provided, use it, otherwise return a fallback
        return obj.source_url if obj.source_url else f"/media/{obj.img_page_url}/{obj.img_tag_id}"


class WebcamHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WebcamHistory
        fields = ['id', 'webcam', 'timestamp', 'image', 'video']

    def to_representation(self, instance):
        # Override to_representation to include the image or video URL
        data = super().to_representation(instance)
        if instance.image:
            data['image_url'] = instance.image.url
        elif instance.video:
            data['video_url'] = instance.video.url
        else:
            data['image_url'] = None
            data['video_url'] = None
        return data
