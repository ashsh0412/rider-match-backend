from django.urls import path
from .views import UserLocationView, PublicLocationView, LocationDetailView

urlpatterns = [
    path("", UserLocationView.as_view(), name="location-list"),
    path("get/", PublicLocationView.as_view(), name="public-location-list"),
    path("get/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
]
