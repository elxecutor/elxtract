from django.urls import path
from .views import DownloadMP4View, AvailableFormatsView, CleanupView

urlpatterns = [
    path("formats/", AvailableFormatsView.as_view(), name="list_formats"),
    path("download/", DownloadMP4View.as_view(), name="download_video"),
    path("cleanup/", CleanupView.as_view(), name="cleanup_downloads"),
]
