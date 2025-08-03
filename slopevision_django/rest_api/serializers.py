from rest_framework import serializers
from .models import Place, Webcam, WebcamHistory
from rest_api.models import CustomUser
from .fields import Base64ImageField
from dj_rest_auth.serializers import UserDetailsSerializer


class PlaceSerializer(serializers.ModelSerializer):
    first_webcam_url = serializers.SerializerMethodField()
    latest_webcam_history = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'name', 'latitude', 'longitude', 'description',
                  'first_webcam_url', 'country', 'nearest_city', 'mounain_range',
                  'latest_webcam_history']

    def get_first_webcam_url(self, obj):
        webcams = list(obj.webcams.all())  # Uses prefetch cache
        return webcams[0].source_url if webcams else None

    def get_latest_webcam_history(self, obj):
        webcams = list(obj.webcams.all())
        if webcams:
            latest_history = webcams[0].latest_history  # Already prefetched
            return latest_history.url if latest_history else None
        return None


class WebcamSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    latest_history_url = serializers.SerializerMethodField()

    class Meta:
        model = Webcam
        fields = ['id', 'place', 'name', 'url', 'source_type', 'source_url', 'page_url',
                  'img_page_url', 'img_tag_id', 'last_updated', 'history_rate', 'latest_history_url']

    def get_latest_history_url(self, obj):
        return obj.latest_history.url if obj.latest_history else None


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


class CustomUserSerializer(UserDetailsSerializer):
    name = serializers.CharField(source='get_full_name')
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    account_type = serializers.CharField(required=False)
    profile_picture = Base64ImageField(required=False, allow_null=True)
    favorite_places = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Place.objects.all(),
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'date_joined',
                  'account_type', 'profile_picture', 'favorite_places']
        read_only_fields = ['username', 'email', 'date_joined']

    def update(self, instance, validated_data):
        # Extract name from validated_data if it exists
        name = validated_data.pop('get_full_name', None)
        if name:
            # Split the name into first_name and last_name
            first_name, last_name = name.split(
                ' ', 1) if ' ' in name else (name, '')
            instance.first_name = first_name
            instance.last_name = last_name

        # Continue with the default update process
        return super().update(instance, validated_data)
