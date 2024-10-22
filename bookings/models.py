from django.db import models


class Booking(models.Model):

    rider = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rider_bookings",
        null=True,
        blank=True,
    )
    passenger = models.ManyToManyField(
        "users.User",
        related_name="passenger_bookings",
    )
    pickup_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    guests = models.PositiveSmallIntegerField(default=1)

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )
    pickup_location = models.CharField(max_length=100, null=True)
    dropoff_location = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.rider} / {self.passenger}"
