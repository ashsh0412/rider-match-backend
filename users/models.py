from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_rider = models.BooleanField(default=False)
