import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Check if the incoming data is a Base64 string
        if isinstance(data, str) and data.startswith('data:image'):
            # Decode the Base64 string
            format, imgstr = data.split(';base64,')  # Format -> data:image/png, etc.
            ext = format.split('/')[-1]  # Get the image file extension (png, jpeg, etc.)
            # Generate a unique filename
            file_name = f"{uuid.uuid4()}.{ext}"
            # Decode the image
            data = ContentFile(base64.b64decode(imgstr), name=file_name)

        return super().to_internal_value(data)
