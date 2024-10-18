from django.urls import path
from .views import MyBooking

urlpatterns = [
    path("", MyBooking.as_view())
]