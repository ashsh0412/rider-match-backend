from rest_framework import serializers
from .models import Booking
from users.models import User  # User 모델이 위치한 경로에 맞게 수정


# User 모델을 직렬화하는 Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


# Booking 모델을 직렬화하는 Serializer
class BookingSerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)  # 라이더 정보 포함

    class Meta:
        model = Booking
        fields = (
            "id",
            "rider",  # 직렬화된 rider 객체 포함
            "driver_name",
            "passengers",
            "pickup_times",
            "locations",
            "guests",
            "created_at",
            "starting_point",
            "arrival_time",
            "departure_time",
            "map_url",
        )
        read_only_fields = ("id", "rider", "created_at")
