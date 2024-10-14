from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pickup_time",
        "guests",
        "type",
        "created_at",
    )
