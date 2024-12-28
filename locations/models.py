from django.db import models
from users.models import User


class Location(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start_latitude = models.FloatField()
    start_longitude = models.FloatField()
    end_latitude = models.FloatField()
    end_longitude = models.FloatField()
    pickup_location = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )
    dropoff_location = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    date_time = models.DateTimeField(
        null=True,
        blank=True,
    )
