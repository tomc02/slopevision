from django.core.management.base import BaseCommand
from rest_api.models import WebcamHistory

class Command(BaseCommand):
    help = 'Clears the history for all webcams.'

    def handle(self, *args, **kwargs):
        try:
            # Count the number of history records before deletion
            history_count = WebcamHistory.objects.count()

            # Delete all WebcamHistory records
            WebcamHistory.objects.all().delete()

            self.stdout.write(self.style.SUCCESS(
                f"Successfully cleared {history_count} webcam history records."
            ))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
