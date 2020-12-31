import cloudinary
from django import forms
from django.conf import settings


class CloudinaryField(forms.FileField):
    def to_python(self, data):
        file = super().to_python(data)
        res = cloudinary.uploader.upload(file, folder=settings.CLOUDINARY_BUCKET)
        image_url = res['public_id']
        return image_url
