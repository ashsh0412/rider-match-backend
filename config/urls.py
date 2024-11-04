from django.contrib import admin
from django.urls import path, include
from apis import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/bookings", include("bookings.urls")),
    path("api/vi/locations", include("locations.urls")),
    path("maps/config/", views.get_maps_config, name="maps-config"),
]
