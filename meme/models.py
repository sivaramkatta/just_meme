from django.db import models
from config.utils import TimestampMixin
from user.models import User
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Meme(TimestampMixin):
    image = models.FileField()
    description = models.TextField()
    posted_by = models.ForeignKey(User, related_name="posts", on_delete=models.DO_NOTHING)
    liked_by = models.ManyToManyField(User, related_name="memes_liked")
    commented_by = models.ManyToManyField(User, related_name="memes_commented", through="Comments")
    category = models.ForeignKey("Category", related_name="memes", on_delete=models.CASCADE)
    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    class Meta:
        ordering = ["-modified"]

    @property
    def meme_image(self):
        return settings.CLOUDINARY_ENDPOINT + self.image.name


class Comments(TimestampMixin):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)

    class Meta:
        ordering = ["-modified"]


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
