from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "start_latitude",
        "start_longitude",
        "end_latitude",
        "end_longitude",
        "pickup_location",
        "dropoff_location",
        "first_name",
        "last_name",
        "date_time",
    )
