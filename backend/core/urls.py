from django.urls import path
from .views import DownloadMP4View, AvailableFormatsView

urlpatterns = [
    path("formats/", AvailableFormatsView.as_view(), name="list_formats"),
    path("download/", DownloadMP4View.as_view(), name="download_video"),
]
