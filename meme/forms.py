from django import forms
from .models import Meme
from config.forms import CloudinaryField


class MemeUploadForm(forms.ModelForm):
    image = CloudinaryField()

    class Meta:
        model = Meme
        fields = ("image", "description", "category", "tags")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemeUploadForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = False
        obj = super(MemeUploadForm, self).save(*args, **kwargs)
        if self.request:
            obj.posted_by = self.request.user
        obj.save()
        return obj
