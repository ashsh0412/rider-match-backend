from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from rest_framework.exceptions import NotFound
from bookings.models import Booking
from django.db.models import Q
import json


class MyBooking(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get bookings where user is the rider
        bookings = Booking.objects.filter(rider=request.user)

        # Get bookings where user is in passengers
        # Using JSONField lookups that work across different database backends
        user_id_str = str(request.user.id)
        passenger_bookings = Booking.objects.filter(
            Q(
                passengers__icontains=user_id_str
            )  # This will do a text search within the JSON
        ).exclude(
            passengers__isnull=True
        )  # Exclude null values

        # Combine the querysets
        all_bookings = (bookings | passenger_bookings).distinct()

        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")

        serializer = BookingSerializer(all_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(rider=request.user)

            # Handle passengers data
            passengers = request.data.get("passengers")
            if passengers:
                # Ensure passengers is properly formatted as JSON
                if isinstance(passengers, str):
                    try:
                        passengers = json.loads(passengers)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid passengers data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.passengers = passengers

            # Handle pickup_times data
            pickup_times = request.data.get("pickup_times")
            if pickup_times:
                # Ensure pickup_times is properly formatted as JSON
                if isinstance(pickup_times, str):
                    try:
                        pickup_times = json.loads(pickup_times)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid pickup_times data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.pickup_times = pickup_times

            # Handle locations data
            locations = request.data.get("locations")
            if locations:
                # Ensure locations is properly formatted as JSON
                if isinstance(locations, str):
                    try:
                        locations = json.loads(locations)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid locations data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.locations = locations

            booking.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Get bookings where user is the rider
        bookings = Booking.objects.filter(rider=request.user)

        # Get bookings where user is in passengers
        user_id_str = str(request.user.id)
        passenger_bookings = Booking.objects.filter(
            Q(passengers__icontains=user_id_str)
        ).exclude(passengers__isnull=True)

        # Combine the querysets
        all_bookings = (bookings | passenger_bookings).distinct()

        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")

        all_bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
