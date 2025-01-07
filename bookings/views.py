from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from bookings.models import Booking
from django.db.models import Q
import json
from datetime import datetime

class MyBooking(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 사용자가 운전자인 예약 조회
        bookings = Booking.objects.filter(rider=request.user)

        # 사용자가 탑승자로 포함된 예약 조회
        user_id_str = str(request.user.id)
        passenger_bookings = Booking.objects.filter(
            passengers__icontains=user_id_str
        ).exclude(passengers__isnull=True)

        # 두 쿼리셋 병합 및 중복 제거
        all_bookings = (bookings | passenger_bookings).distinct().order_by("created_at")

        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")

        serializer = BookingSerializer(all_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(rider=request.user)

            # 탑승자 데이터 처리
            passengers = request.data.get("passengers", [])
            if isinstance(passengers, str):
                try:
                    passengers = json.loads(passengers)
                except json.JSONDecodeError:
                    return Response(
                        {"error": "Invalid passengers data format"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            booking.passengers = passengers

            # 픽업 시간 데이터 처리 - 포맷 지정
            pickup_times = request.data.get("pickup_times", [])
            if isinstance(pickup_times, str):
                try:
                    pickup_times = json.loads(pickup_times)
                except json.JSONDecodeError:
                    return Response(
                        {"error": "Invalid pickup_times data format"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # 변환 없이 그대로 저장
            booking.pickup_times = pickup_times

            # 위치 데이터 처리
            locations = request.data.get("locations", {})
            if isinstance(locations, str):
                try:
                    locations = json.loads(locations)
                except json.JSONDecodeError:
                    return Response(
                        {"error": "Invalid locations data format"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            booking.locations = locations

            # 게스트 수 업데이트
            if passengers:
                booking.guests = len(passengers)

            # 운전자 이름 설정
            if request.user:
                booking.driver_name = f"{request.user.first_name} {request.user.last_name}"

            booking.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateBooking(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise NotFound("Booking not found")

        # 운전자나 탑승자만 수정 가능
        if (
            booking.rider != request.user
            and str(request.user.id) not in booking.passengers
        ):
            raise PermissionDenied("You do not have permission to update this booking")

        serializer = BookingSerializer(booking, data=request.data, partial=True)

        if serializer.is_valid():
            booking = serializer.save()

            # 시간 데이터 처리
            pickup_times = request.data.get("pickup_times")
            if pickup_times:
                if isinstance(pickup_times, str):
                    pickup_times = json.loads(pickup_times)
                
                formatted_pickup_times = []
                for time in pickup_times:
                    try:
                        dt = datetime.fromisoformat(time.replace('Z', '+00:00'))
                        formatted_time = dt.strftime("%b %d, %Y, %I:%M %p")
                        formatted_pickup_times.append(formatted_time)
                    except ValueError:
                        return Response(
                            {"error": f"Invalid time format: {time}"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.pickup_times = formatted_pickup_times

            # 기본 필드 업데이트
            for field in ["passengers", "locations"]:
                data = request.data.get(field)
                if data:
                    if isinstance(data, str):
                        data = json.loads(data)
                    setattr(booking, field, data)

            # 운전자 변경 처리
            new_rider_id = request.data.get("rider")
            if new_rider_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    new_rider = User.objects.get(id=new_rider_id)
                    booking.rider = new_rider
                    booking.driver_name = f"{new_rider.first_name} {new_rider.last_name}"
                except User.DoesNotExist:
                    return Response(
                        {"error": "New rider not found"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # 게스트 수 업데이트
            if "passengers" in request.data:
                booking.guests = len(booking.passengers)

            booking.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)