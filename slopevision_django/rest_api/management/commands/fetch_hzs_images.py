from django.core.management.base import BaseCommand
from rest_api.models import Webcam
from rest_api.utils import get_image_urls_sync, save_webcam_url
class Command(BaseCommand):
    help = 'Fetch video URLs for each webcam model and update the description'

    def handle(self, *args, **kwargs):
        image_ids = []
        # Get all webcam objects with source_type IMG_TAG and img_page_url containing 'meteo.hzs'
        hzs_webcams = Webcam.objects.filter(source_type='IMG_TAG', img_page_url__contains='meteo.hzs')
        for model in hzs_webcams:
            image_ids.append(model.img_tag_id)

        urls = get_image_urls_sync(image_ids)
        for model in hzs_webcams:
            image_url = urls.get(model.img_tag_id)
            save_webcam_url(model, image_url)


