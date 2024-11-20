from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_rider = models.BooleanField(default=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": ("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        unique=True,  # 유니크한 이메일
        error_messages={
            "unique": ("A user with that email address already exists."),
        },
    )
