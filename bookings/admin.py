from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['rider', 'driver_name', 'pickup_times', 'guests', 'created_at']
    list_filter = ['created_at', 'guests']
    search_fields = ['rider__username', 'driver_name']
    readonly_fields = ['created_at']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['passengers'].widget.attrs['style'] = 'width: 45em; height: 5em;'
        form.base_fields['pickup_times'].widget.attrs['style'] = 'width: 45em; height: 5em;'
        form.base_fields['locations'].widget.attrs['style'] = 'width: 45em; height: 5em;'
        return form