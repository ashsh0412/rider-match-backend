from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "rider",
            "driver_name",
            "passengers",
            "pickup_times",
            "locations",
            "guests",
            "created_at",
        )
        read_only_fields = ("id", "rider", "created_at")