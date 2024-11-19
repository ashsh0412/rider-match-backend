from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from bookings.models import Booking
from django.db.models import Q
import json


class MyBooking(APIView):
    """
    예약 관리를 위한 API 뷰
    인증된 사용자만 접근 가능
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        현재 사용자의 모든 예약을 조회
        - 사용자가 운전자인 예약
        - 사용자가 탑승자로 포함된 예약
        """
        # 사용자가 운전자인 예약 조회
        bookings = Booking.objects.filter(rider=request.user)

        # 사용자가 탑승자로 포함된 예약 조회
        user_id_str = str(request.user.id)
        passenger_bookings = Booking.objects.filter(
            Q(passengers__icontains=user_id_str)
        ).exclude(passengers__isnull=True)

        # 두 쿼리셋 병합 및 중복 제거
        all_bookings = (bookings | passenger_bookings).distinct()

        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")

        serializer = BookingSerializer(all_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        새로운 예약 생성
        - passengers: 탑승자 목록 (JSON 형식)
        - pickup_times: 픽업 시간 목록 (JSON 형식)
        - locations: 위치 정보 목록 (JSON 형식)
        """
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            # 현재 사용자를 운전자로 설정하여 예약 생성
            booking = serializer.save(rider=request.user)

            # 탑승자 데이터 처리
            passengers = request.data.get("passengers")
            if passengers:
                if isinstance(passengers, str):
                    try:
                        # 문자열로 전달된 JSON 데이터 파싱
                        passengers = json.loads(passengers)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid passengers data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.passengers = passengers

            # 픽업 시간 데이터 처리
            pickup_times = request.data.get("pickup_times")
            if pickup_times:
                if isinstance(pickup_times, str):
                    try:
                        pickup_times = json.loads(pickup_times)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid pickup_times data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.pickup_times = pickup_times

            # 위치 데이터 처리
            locations = request.data.get("locations")
            if locations:
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

    def put(self, request, booking_id):
        """
        기존 예약 수정
        - 운전자나 탑승자만 수정 가능
        - 부분 업데이트 지원 (일부 필드만 수정 가능)
        """
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise NotFound("Booking not found")

        # 권한 확인: 운전자이거나 탑승자여야 함
        if (
            booking.rider != request.user
            and str(request.user.id) not in booking.passengers
        ):
            raise PermissionDenied("You do not have permission to update this booking")

        # 예약 데이터 업데이트
        serializer = BookingSerializer(booking, data=request.data, partial=True)

        if serializer.is_valid():
            booking = serializer.save()

            # 탑승자 데이터 업데이트
            passengers = request.data.get("passengers")
            if passengers:
                if isinstance(passengers, str):
                    try:
                        passengers = json.loads(passengers)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid passengers data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.passengers = passengers

            # 픽업 시간 데이터 업데이트
            pickup_times = request.data.get("pickup_times")
            if pickup_times:
                if isinstance(pickup_times, str):
                    try:
                        pickup_times = json.loads(pickup_times)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid pickup_times data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.pickup_times = pickup_times

            # 위치 데이터 업데이트
            locations = request.data.get("locations")
            if locations:
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
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        현재 사용자와 관련된 모든 예약 삭제
        - 운전자로 등록된 예약
        - 탑승자로 등록된 예약
        """
        bookings = Booking.objects.filter(rider=request.user)
        user_id_str = str(request.user.id)
        passenger_bookings = Booking.objects.filter(
            Q(passengers__icontains=user_id_str)
        ).exclude(passengers__isnull=True)

        all_bookings = (bookings | passenger_bookings).distinct()

        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")

        all_bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateBooking(APIView):
    """
    특정 예약 수정 API
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        """
        예약 수정 - booking_id 기반으로 업데이트
        """

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            raise NotFound("Booking not found")

        # 권한 확인: 운전자이거나 탑승자여야 함
        if (
            booking.rider != request.user
            and str(request.user.id) not in booking.passengers
        ):
            raise PermissionDenied("You do not have permission to update this booking")

        # 예약 데이터 업데이트
        serializer = BookingSerializer(booking, data=request.data, partial=True)

        if serializer.is_valid():
            booking = serializer.save()

            # 탑승자 정보 업데이트
            passengers = request.data.get("passengers")
            if passengers:
                if isinstance(passengers, str):
                    try:
                        passengers = json.loads(passengers)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid passengers data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.passengers = passengers

            # 픽업 시간 정보 업데이트
            pickup_times = request.data.get("pickup_times")
            if pickup_times:
                if isinstance(pickup_times, str):
                    try:
                        pickup_times = json.loads(pickup_times)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid pickup_times data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.pickup_times = pickup_times

            # 위치 정보 업데이트
            locations = request.data.get("locations")
            if locations:
                if isinstance(locations, str):
                    try:
                        locations = json.loads(locations)
                    except json.JSONDecodeError:
                        return Response(
                            {"error": "Invalid locations data format"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                booking.locations = locations

            # 운전자 업데이트 (옵션)
            new_rider_id = request.data.get("rider")
            if new_rider_id:
                booking.rider_id = new_rider_id

            booking.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
