from django.db import models

class DownloadRequest(models.Model):
    url = models.URLField()
    format = models.CharField(max_length=10, default='mp4')
    video_id = models.CharField(max_length=128, unique=True)
    filename = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} -> {self.filename}"
