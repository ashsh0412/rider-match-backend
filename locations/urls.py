from django.urls import path
from .views import LocationView, PublicLocationView

urlpatterns = [
    path(
        "",
        LocationView.as_view(),
    ),
    path(
        "get",
        PublicLocationView.as_view(),
    ),
]
