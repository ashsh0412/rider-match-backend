from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import BookingSerializer
from rest_framework.exceptions import NotFound, ParseError
from bookings.models import Booking
from django.db.models import Q

class MyBooking(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 사용자가 rider인 예약과 passengers에 포함된 예약을 찾습니다
        bookings = Booking.objects.filter(rider=request.user)
        passenger_bookings = Booking.objects.filter(
            passengers__contains=str(request.user.id)  # JSONField에서 검색
        )
        all_bookings = bookings | passenger_bookings
        
        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")
        
        serializer = BookingSerializer(all_bookings, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        
        if serializer.is_valid():
            # rider는 현재 로그인한 사용자로 자동 설정
            booking = serializer.save(rider=request.user)
            
            # passengers 데이터가 있는 경우 처리
            passengers = request.data.get('passengers')
            if passengers:
                booking.passengers = passengers
            
            # pickup_times 데이터가 있는 경우 처리
            pickup_times = request.data.get('pickup_times')
            if pickup_times:
                booking.pickup_times = pickup_times
            
            # locations 데이터가 있는 경우 처리
            locations = request.data.get('locations')
            if locations:
                booking.locations = locations
            
            booking.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        bookings = Booking.objects.filter(rider=request.user)
        passenger_bookings = Booking.objects.filter(
            passengers__contains=str(request.user.id)
        )
        all_bookings = bookings | passenger_bookings
        
        if not all_bookings.exists():
            raise NotFound("No bookings found for this user")
        
        all_bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)