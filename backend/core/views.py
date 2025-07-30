import os
import hashlib
import yt_dlp
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import DownloadRequest
from django.conf import settings

# View to fetch available formats
class AvailableFormatsView(APIView):
    def post(self, request):
        url = request.data.get("url")
        if not url:
            return Response({"error": "URL is required."}, status=400)

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = [
                    {
                        "format_id": f["format_id"],
                        "resolution": f.get("height"),
                        "ext": f["ext"],
                        "note": f["format_note"],
                        "filesize": f.get("filesize"),
                    }
                    for f in info["formats"]
                    if f["ext"] == "mp4" and f.get("vcodec") != "none" and f.get("acodec") != "none"
                ]
                formats = sorted(formats, key=lambda x: x["resolution"] or 0)
                return Response({"formats": formats})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# Utility to generate hash-based ID if needed
def get_video_id(url):
    return hashlib.sha256(url.encode()).hexdigest()

# View to download MP4 using actual video title
class DownloadMP4View(APIView):
    def post(self, request):
        url = request.data.get("url")
        format_id = request.data.get("format_id")
        if not url or not format_id:
            return Response({"error": "URL and format_id are required."}, status=400)

        output_dir = os.path.join(settings.MEDIA_ROOT, "downloads")
        os.makedirs(output_dir, exist_ok=True)

        # Use title in output filename, fallback to ID to avoid collision
        output_template = os.path.join(output_dir, "%(title).100s-%(id)s.%(ext)s")

        try:
            ydl_opts = {
                "format": format_id,
                "outtmpl": output_template,
                "quiet": True,
                "noplaylist": True,
                "merge_output_format": "mp4",
                "restrictfilenames": True,  # avoid problematic characters
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # Enforce .mp4 if required (yt-dlp may not add it in some cases)
                if not filename.endswith(".mp4"):
                    filename = filename.rsplit(".", 1)[0] + ".mp4"

                filename = os.path.basename(filename)
                video_id = get_video_id(f"{url}_{format_id}")

            # Store or update record
            DownloadRequest.objects.get_or_create(
                url=url,
                format="mp4",
                video_id=video_id,
                filename=filename
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        file_url = f"{request.scheme}://{request.get_host()}/media/downloads/{filename}"
        return Response({"download_url": file_url})
