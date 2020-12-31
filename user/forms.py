from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import login


class SignUPForm(UserCreationForm):
    first_name = forms.CharField(initial="", max_length=100, widget=forms.TextInput(attrs={'autofocus': ''}))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SignUPForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit'] = True
        obj = super(SignUPForm, self).save(*args, **kwargs)
        login(self.request, obj)
        return obj


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
