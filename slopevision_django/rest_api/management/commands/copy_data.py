from django.core.management.base import BaseCommand
from django.db import connections
from django.apps import apps

class Command(BaseCommand):
    help = 'Copy data from old database to new database, excluding users and groups'

    def handle(self, *args, **kwargs):
        old_db = 'old_db'
        new_db = 'default'

        # List of app labels and models to include
        include_models = [
            model for model in apps.get_models()
            if model._meta.app_label == 'rest_api'
        ]
        # exlude rest_api.models.CustomUser
        include_models = [model for model in include_models if model._meta.object_name != 'CustomUser']

        for model in include_models:
            self.stdout.write(f"Copying data for {model._meta.label}...")

            # Fetch all data from the old database
            objects = model.objects.using(old_db).all()

            # Bulk create in the new database
            model.objects.using(new_db).bulk_create(objects)

        self.stdout.write(self.style.SUCCESS("Data copy completed successfully."))
