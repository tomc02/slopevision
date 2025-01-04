import os
import subprocess
from time import sleep
from urllib.parse import urlparse

import cv2
import requests
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from google.cloud import storage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from rest_api.models import Webcam, WebcamHistory


class Command(BaseCommand):
    help = "Save all active webcams to history based on their current URL."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize Google Cloud Storage client
        self.storage_client = storage.Client()
        self.bucket_name = 'slopevision-dev'  # Replace with your bucket name
        self.bucket = self.storage_client.bucket(self.bucket_name)

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
                        self._save_file_to_gcs(response, f'webcam_images/{file_name}')
                        WebcamHistory.objects.create(webcam=webcam, image=f'webcam_images/{file_name}')
                        self.stdout.write(f"Saved image for webcam '{webcam.name}' (ID: {webcam.id}).")

                    elif 'video' in content_type:
                        # Save video locally
                        local_video_path = f'/tmp/{file_name}'
                        with open(local_video_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)

                        # Compress video using ffmpeg
                        compressed_video_path = f'/tmp/compressed_{file_name}'
                        self._compress_video(local_video_path, compressed_video_path)

                        # Upload compressed video to Google Cloud Storage
                        self._save_file_to_gcs_with_local_path(compressed_video_path, f'webcam_videos/{file_name}')
                        WebcamHistory.objects.create(webcam=webcam, video=f'webcam_videos/{file_name}')
                        self.stdout.write(
                            f"Saved and uploaded compressed video for webcam '{webcam.name}' (ID: {webcam.id}).")

                    else:
                        cap = cv2.VideoCapture(url)
                        if not cap.isOpened():
                            self.stdout.write(
                                f"Failed to open video stream for webcam '{webcam.name}' (ID: {webcam.id}).")
                        else:
                            ret, frame = cap.read()
                            if ret:
                                file_name = f'webcam_images/{webcam.id}_{timestamp}.jpg'
                                self._save_frame_to_gcs(frame, file_name)
                                WebcamHistory.objects.create(webcam=webcam, image=file_name)
                                self.stdout.write(f"Saved image for webcam '{webcam.name}' (ID: {webcam.id}).")
                            else:
                                self.stdout.write(
                                    f"Failed to capture frame for webcam '{webcam.name}' (ID: {webcam.id}).")
                            cap.release()

            except requests.RequestException as e:
                self.stderr.write(f"Failed to fetch URL for webcam '{webcam.name}' (ID: {webcam.id}): {e}")

    def _is_embed_url(self, url):
        """Check if the URL is an embedded content page."""
        return 'embed' in url or '.html' in url

    def _capture_embed_screenshot(self, webcam, url):
        """Use a headless browser to capture a screenshot of an embedded page."""
        timestamp = now().strftime('%Y%m%d%H%M%S')
        file_name = f'webcam_images/{webcam.id}_{timestamp}.png'

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280x720")

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(url)
            sleep(15)  # Wait for the page to load
            png = driver.get_screenshot_as_png()

            # Save screenshot to Google Cloud Storage
            self._save_bytes_to_gcs(png, file_name)

        WebcamHistory.objects.create(webcam=webcam, image=file_name)
        self.stdout.write(f"Saved screenshot for embedded webcam '{webcam.name}' (ID: {webcam.id}).")

    def _save_file_to_gcs(self, response, file_name):
        """Upload streamed content to Google Cloud Storage."""
        blob = self.bucket.blob(file_name)
        blob.upload_from_file(response.raw, content_type=response.headers.get('Content-Type'))
        self.stdout.write(f"Uploaded {file_name} to Google Cloud Storage.")

    def _save_frame_to_gcs(self, frame, file_name):
        """Save a video frame to Google Cloud Storage."""
        blob = self.bucket.blob(file_name)
        _, buffer = cv2.imencode('.jpg', frame)
        blob.upload_from_string(buffer.tobytes(), content_type='image/jpeg')
        self.stdout.write(f"Uploaded {file_name} to Google Cloud Storage.")

    def _save_bytes_to_gcs(self, content, file_name):
        """Save raw bytes to Google Cloud Storage."""
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(content)
        self.stdout.write(f"Uploaded {file_name} to Google Cloud Storage.")

    def _compress_video(self, input_path, output_path):
        """Compress video using ffmpeg."""
        # f'ffmpeg -i {full_path} -vf "scale=640:-1,fps=10" -c:v libx264 -crf 35 -an {compressed_path}')
        cmd = ['ffmpeg', '-i', input_path, '-vf', 'scale=640:-1,fps=10', '-c:v', 'libx264', '-crf', '35', '-an', output_path]
        # Wait for the process to finish and check for errors
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Ensure that the process completes successfully
        if result.returncode == 0:
            self.stdout.write(f"Video compression finished. Compressed video saved to {output_path}.")
        else:
            self.stderr.write(f"Error compressing video: {result.stderr.decode()}")

    def _save_file_to_gcs_with_local_path(self, local_path, file_name):
        """Upload a local file to Google Cloud Storage."""
        blob = self.bucket.blob(file_name)
        # Ensure the file exists before uploading
        if os.path.exists(local_path):
            blob.upload_from_filename(local_path)
            self.stdout.write(f"Uploaded {file_name} to Google Cloud Storage.")
        else:
            self.stderr.write(f"File {local_path} does not exist, skipping upload.")
