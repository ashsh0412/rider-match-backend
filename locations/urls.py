from django.urls import path
from .views import Location

urlpatterns = [path("", Location.as_view())]
