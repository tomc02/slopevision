from django.db import models
from django.contrib.gis.db import models as gis_models

class Place(models.Model):
    """
    A geographical location that can have webcams and weather forecasts.
    """
    name = models.CharField(max_length=255)
    geolocation = gis_models.PointField()  # PointField for latitude and longitude
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100)
    nearest_city = models.CharField(max_length=100, blank=True, null=True)
    mounain_range = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
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

    def __str__(self):
        return self.name

class WebcamHistory(models.Model):
    """
    Historical snapshots of webcam data (e.g., image or video link).
    """
    webcam = models.ForeignKey(Webcam, on_delete=models.CASCADE, related_name='history')
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='webcam_images', blank=True, null=True)
    video = models.FileField(upload_to='webcam_videos', blank=True, null=True)

    def __str__(self):
        return f"Snapshot for {self.webcam.name} at {self.timestamp}"