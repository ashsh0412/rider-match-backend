from rest_framework.serializers import ModelSerializer
from .models import Location


# serializers.py
class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = [
            "id",
            "user",
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude",
            "address",
            "first_name",
            "last_name",
        ]
