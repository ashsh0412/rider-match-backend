from django.urls import path
from .views import MyBooking

urlpatterns = [
    path(
        "my-bookings/",  # 빈 문자열("") 대신 더 명확한 경로
        MyBooking.as_view(),
        name="my-bookings"  # URL 패턴의 이름 추가
    ),
]