from django.db import models
import uuid
from config.utils import TimestampMixin
from django.contrib.auth.models import AbstractUser


class User(TimestampMixin, AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, default='User')
    email = models.EmailField(unique=True)
