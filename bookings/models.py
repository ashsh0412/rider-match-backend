from django.db import models
from django.utils import timezone


class Booking(models.Model):
    rider = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rider_bookings",
        null=True,
        blank=True,
    )
    driver_name = models.CharField(max_length=1000, null=True, blank=True)
    passengers = models.JSONField(null=True, blank=True)  # [{"id": 1, "name": "John"}]
    pickup_times = models.JSONField(null=True, blank=True)  # ["2024-03-15T14:30"]
    locations = models.JSONField(null=True, blank=True)
    guests = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    starting_point = models.CharField(max_length=1000, null=True, blank=True)
    map_url = models.URLField(null=True, blank=True, max_length=2000)

    def __str__(self):
        return f"{self.rider} / {self.passengers}"
