from django.db import models


class Booking(models.Model):
    class BookingTypeChoices(models.TextChoices):
        RIDER = ("rider", "Rider")
        DRIVER = ("driver", "Driver")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    pickup_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveSmallIntegerField(default=1)
    type = models.CharField(
        max_length=6,
        choices=BookingTypeChoices,
        default="rider",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    pickup_location = models.CharField(max_length=100, null=True)
    dropoff_location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.type} / {self.user}"
