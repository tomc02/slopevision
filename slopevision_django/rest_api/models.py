from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True, default='default_profile_picture.png')
    ACCOUNT_TYPE_CHOICES = (
        ('free', 'Free'),
        ('premium', 'Premium'),
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='premuim')
    favorite_places = models.ManyToManyField('Place', blank=True, related_name='favorited_by')


class Place(models.Model):
    """
    A geographical location that can have webcams and weather forecasts.
    """
    name = models.CharField(max_length=255)
    latitude = models.FloatField()  # Latitude coordinate
    longitude = models.FloatField()  # Longitude coordinate
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100)
    nearest_city = models.CharField(max_length=100, blank=True, null=True)
    mounain_range = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_geolocation(self):
        return (self.latitude, self.longitude)


class Webcam(models.Model):
    """
    A webcam associated with a specific place.
    """
    API = 'API'
    IPCAM = 'IPCAM'
    SCRAPE = 'SCRAPE'
    IMG_TAG = 'IMG_TAG'

    WEB_CAM_CHOICES = [
        (API, 'API'),
        (IPCAM, 'IP Camera'),
        (SCRAPE, 'Scraped Video'),
        (IMG_TAG, 'Image Tag'),
    ]

    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='webcams')
    source_type = models.CharField(
        max_length=10,
        choices=WEB_CAM_CHOICES,
        default=IPCAM,
    )

    # The URL that corresponds to the webcam source
    # For API and IP Camera, this could be an endpoint or stream URL
    source_url = models.URLField(max_length=1000, blank=True, null=True)

    # For SCRAPE source, we save the page URL (where to scrape video)
    page_url = models.URLField(max_length=200, blank=True, null=True)

    # For IMG_TAG source, we save the page URL and the image's unique identifier (img ID)
    img_page_url = models.URLField(max_length=200, blank=True, null=True)
    img_tag_id = models.CharField(max_length=100, blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)
    history_rate = models.PositiveIntegerField(
        default=30,
        help_text="Time interval in minutes for history updates (e.g., every 30 minutes)."
    )
    
    latest_history = models.ForeignKey(
    'WebcamHistory',
    on_delete=models.SET_NULL,
    blank=True,
    null=True,
    related_name='latest_history_webcam'
    )

    @property
    def url(self):
        return self.source_url if self.source_url else f"/media/{self.img_page_url}/{self.img_tag_id}"

    def __str__(self):
        return f"{self.name} ({self.place.name})"


class WebcamHistory(models.Model):
    """
    Historical snapshots of webcam data (e.g., image or video link).
    """

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['webcam', '-timestamp']),
        ]

    webcam = models.ForeignKey(Webcam, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the snapshot")
    image = models.ImageField(upload_to='webcam_images', blank=True, null=True)
    video = models.FileField(upload_to='webcam_videos', blank=True, null=True)

    def __str__(self):
        return f"Snapshot for {self.webcam.name} at {self.timestamp}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Update the latest history for the webcam
        if self.webcam:
            self.webcam.latest_history = self
            self.webcam.save(update_fields=['latest_history'])
            
    @property
    def url(self):
        if self.image:
            return self.image.url
        elif self.video:
            return self.video.url
        return None
