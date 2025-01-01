from time import sleep

from django.core.management.base import BaseCommand
from django.utils.timezone import now
import os
import requests
from urllib.parse import urlparse
from rest_api.models import Webcam, WebcamHistory
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO


class Command(BaseCommand):
    help = "Save all active webcams to history based on their current URL."

    def handle(self, *args, **kwargs):
        active_webcams = Webcam.objects.all()
        self.stdout.write(f"Found {active_webcams.count()} active webcams.")

        for webcam in active_webcams:
            url = webcam.source_url

            if not url:
                self.stdout.write(f"Skipping webcam '{webcam.name}' (ID: {webcam.id}) - No URL provided.")
                continue

            try:
                if self._is_embed_url(url):
                    self._capture_embed_screenshot(webcam, url)
                else:
                    response = requests.get(url, stream=True, verify=False)  # Ignore SSL certificate errors
                    response.raise_for_status()

                    content_type = response.headers.get('Content-Type', '')
                    timestamp = now().strftime('%Y%m%d%H%M%S')
                    file_extension = os.path.splitext(urlparse(url).path)[-1]
                    file_name = f"{webcam.id}_{timestamp}{file_extension}" if file_extension else f"{webcam.id}_{timestamp}"

                    if 'image' in content_type:
                        file_path = f'webcam_images/{file_name}'
                        self._save_file(response, file_path)
                        WebcamHistory.objects.create(webcam=webcam, image=file_path)
                        self.stdout.write(f"Saved image for webcam '{webcam.name}' (ID: {webcam.id}).")

                    elif 'video' in content_type:
                        file_path = f'webcam_videos/{file_name}'
                        self._save_file(response, file_path)
                        WebcamHistory.objects.create(webcam=webcam, video=file_path)
                        self.stdout.write(f"Saved video for webcam '{webcam.name}' (ID: {webcam.id}).")

                    else:
                        cap = cv2.VideoCapture(url)
                        if not cap.isOpened():
                            self.stdout.write(f"Failed to open video stream for webcam '{webcam.name}' (ID: {webcam.id}).")
                        else:
                            ret, frame = cap.read()
                            if ret:
                                file_path = f'webcam_images/{webcam.id}_{timestamp}.jpg'
                                full_path = os.path.join('media', file_path)
                                cv2.imwrite(full_path, frame)
                                WebcamHistory.objects.create(webcam=webcam, image=file_path)
                                self.stdout.write(f"Saved image for webcam '{webcam.name}' (ID: {webcam.id}).")
                            else:
                                self.stdout.write(f"Failed to capture frame for webcam '{webcam.name}' (ID: {webcam.id}).")
                            cap.release()

            except requests.RequestException as e:
                self.stderr.write(f"Failed to fetch URL for webcam '{webcam.name}' (ID: {webcam.id}): {e}")

    def _is_embed_url(self, url):
        """Check if the URL is an embedded content page."""
        return 'embed' in url or '.html' in url

    def _capture_embed_screenshot(self, webcam, url):
        """Use a headless browser to capture a screenshot of an embedded page."""
        timestamp = now().strftime('%Y%m%d%H%M%S')
        file_path = f'webcam_images/{webcam.id}_{timestamp}.png'
        full_path = os.path.join('media', file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280x720")

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(url)
            # Wait 15 seconds for the page to load
            sleep(15)
            png = driver.get_screenshot_as_png()

            # Save screenshot
            image = Image.open(BytesIO(png))
            image.save(full_path, 'PNG')

        WebcamHistory.objects.create(webcam=webcam, image=file_path)
        self.stdout.write(f"Saved screenshot for embedded webcam '{webcam.name}' (ID: {webcam.id}).")

    def _save_file(self, response, file_path):
        """Helper method to save streamed content to a file."""
        full_path = os.path.join('media', file_path)
        compressed_path = os.path.join('media', 'compressed', file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # compress file
        if '.mp4' in file_path:
            os.system(f'ffmpeg -i {full_path} -vf "scale=640:-1,fps=10" -c:v libx264 -crf 35 -an {compressed_path}')
            os.remove(full_path)
            os.rename(compressed_path, full_path)
