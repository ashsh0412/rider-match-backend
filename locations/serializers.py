from rest_framework.serializers import ModelSerializer
from .models import Location


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude",
            "user",
        )
