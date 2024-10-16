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
    guests = models.PositiveSmallIntegerField()
    type = models.CharField(
        max_length=6,
        choices=BookingTypeChoices,
        default="rider",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f"{self.type} / {self.user}"
