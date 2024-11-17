from django.urls import path
from .views import MyBooking, UpdateBooking

urlpatterns = [
    path("my-bookings/", MyBooking.as_view()),
    path("my-bookings/<int:booking_id>/", UpdateBooking.as_view()),  # 특정 예약 수정 및 삭제를 위한 경로
]
