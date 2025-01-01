from django.core.management.base import BaseCommand
from rest_api.models import Webcam
from rest_api.utils import find_video_url, save_webcam_url
class Command(BaseCommand):
    help = 'Fetch video URLs for each webcam model and update the description'

    def handle(self, *args, **kwargs):
        for model in Webcam.objects.filter(source_type='SCRAPE'):
            video_url = find_video_url(model.page_url)
            save_webcam_url(model, video_url)
