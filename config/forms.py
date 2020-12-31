import cloudinary
from django import forms


class CloudinaryField(forms.FileField):
    def to_python(self, data):
        file = super().to_python(data)
        res = cloudinary.uploader.upload(file, folder='just_meme')
        image_url = res['public_id']
        return image_url
