from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "rider",
        "get_passenger",  # ManyToManyField를 처리하는 커스텀 메서드
        "pickup_time",
        "guests",
        "created_at",
    )

    def get_passenger(self, obj):
        return ", ".join([str(p) for p in obj.passenger.all()])  # ManyToManyField로 처리
    get_passenger.short_description = 'Passengers'