from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from rest_api.models import Place, Webcam, WebcamHistory
import sqlite3
import os

class Command(BaseCommand):
    help = 'Migrates data from the old SQLite database to the new models'

    def handle(self, *args, **kwargs):
        # Ask for the path to the old database
        old_db_path = input("Please enter the path to the old SQLite database: ")

        # Validate the path
        if not os.path.exists(old_db_path):
            self.stdout.write(self.style.ERROR(f"The specified database path does not exist: {old_db_path}"))
            return

        if not old_db_path.endswith(".sqlite3"):
            self.stdout.write(self.style.ERROR(f"The specified path does not point to a valid SQLite database: {old_db_path}"))
            return

        self.stdout.write(f"Starting migration from the old database at {old_db_path}...")

        # Connect to the old SQLite database
        conn = sqlite3.connect(old_db_path)
        cursor = conn.cursor()

        # Print all tables in the old database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        self.stdout.write(f"Tables in the old database: {tables}")

        # Migrate Place data
        cursor.execute("SELECT id, name, latitude, longitude, description FROM powcast_web_place")
        places_data = cursor.fetchall()

        for place_data in places_data:
            place_id, name, latitude, longitude, description = place_data

            # Create a Point object for geolocation
            geolocation = Point(longitude, latitude)

            # Insert Place into the new database
            place = Place(
                name=name,
                geolocation=geolocation,
                description=description or '',
                country='Unknown',  # Set to default or your logic
                nearest_city=None,  # Optional: set this based on additional logic
                mounain_range=None,  # Optional: set this based on additional logic
            )
            place.save()

            # Migrate associated webcams
            cursor.execute("SELECT id, place_id, name, url, is_active, image, page_url, page_image_name, description FROM powcast_web_webcam WHERE place_id=?", (place_id,))
            webcams_data = cursor.fetchall()

            for webcam_data in webcams_data:
                webcam_id, old_place_id, name, url, is_active, image, page_url, page_image_name, description = webcam_data

                # Determine the source type (for simplicity, map old URLs to source type)
                source_type = 'IPCAM'  # Default to IPCAM, add logic if needed to map to other types
                source_url = url if url else None
                page_url = page_url if page_url else None
                img_page_url = None
                if page_image_name:
                    source_type = 'IMG_TAG'
                    img_page_url = 'https://meteo.hzs.sk/'  # In OLD DB, there was only one source for IMG cams
                if page_url:
                    source_type = 'SCRAPE'

                # Create a new Webcam entry
                webcam = Webcam(
                    name=name,
                    place=place,
                    source_type=source_type,
                    source_url=source_url,
                    page_url=page_url,
                    img_page_url=img_page_url,
                    img_tag_id=page_image_name,
                    last_updated=None,
                    history_rate=30,  # Default value
                )
                webcam.save()

                # Migrate webcam history
                cursor.execute("SELECT id, webcam_id, timestamp, image, video FROM powcast_web_webcamhistory WHERE webcam_id=?", (webcam_id,))
                history_data = cursor.fetchall()
                for history_entry in history_data:
                    history_id, old_webcam_id, timestamp, image, video = history_entry
                    print(f"Webcam ID: {webcam_id}, History ID: {history_id}, Timestamp: {timestamp}")

                    # Create a new WebcamHistory entry
                    history = WebcamHistory(
                        webcam=webcam,
                        timestamp=timestamp,
                        image=image,  # Assuming you handle image storage migration
                        video=video,  # Assuming you handle video storage migration
                    )
                    history.save(force_insert=True)

        # Close the old database connection
        conn.close()

        self.stdout.write(self.style.SUCCESS('Migration completed successfully!'))
