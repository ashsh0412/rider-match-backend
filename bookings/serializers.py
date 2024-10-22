from rest_framework.serializers import ModelSerializer
from .models import Booking


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "rider",
            "passenger",
            "pickup_time",
            "guests",
            "created_at",
            "pickup_location",
            "dropoff_location",
        )
