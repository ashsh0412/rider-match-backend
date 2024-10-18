from rest_framework.serializers import ModelSerializer
from .models import Booking


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "user",
            "pickup_time",
            "guests",
            "type",
            "created_at",
            "pickup_location",
            "dropoff_location",
        )
