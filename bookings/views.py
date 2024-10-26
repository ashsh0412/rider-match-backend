from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from rest_framework.exceptions import NotFound
from bookings.models import Booking


class MyBooking(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 사용자의 예약 정보를 가져오기 (rider 또는 passenger)
        bookings = Booking.objects.filter(rider=request.user) | Booking.objects.filter(
            passenger=request.user
        )  # rider와 passenger 모두에서 예약을 찾음

        if not bookings.exists():
            raise NotFound("No bookings found for this user")

        # 여러 예약이 있을 수 있으므로 리스트를 직렬화
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def delete(self, request):
        # 현재 사용자의 예약 정보를 가져와 삭제 (rider 또는 passenger)
        bookings = Booking.objects.filter(rider=request.user) | Booking.objects.filter(
            passenger=request.user
        )  # rider와 passenger 모두에서 예약을 찾음

        if not bookings.exists():
            raise NotFound("No bookings found for this user")

        # 예약 삭제
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
