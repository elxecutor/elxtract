import os
import hashlib
import yt_dlp
import threading
import time
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

        import logging
        logger = logging.getLogger(__name__)
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
                # Add video details
                video_details = {
                    "title": info.get("title"),
                    "duration": info.get("duration"),
                    "thumbnail": info.get("thumbnail"),
                }
                return Response({"formats": formats, "video_details": video_details})
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"yt_dlp DownloadError: {e}")
            return Response({"error": "Failed to fetch video info. The video may be unavailable or restricted."}, status=400)
        except Exception as e:
            logger.exception("Unexpected error in AvailableFormatsView")
            return Response({"error": "Internal server error. Please try again later."}, status=500)

# Utility to generate hash-based ID if needed
def get_video_id(url):
    return hashlib.sha256(url.encode()).hexdigest()

# Utility function to delete file after specified time
def delete_file_after_delay(file_path, delay_hours):
    """Delete a file after a specified delay in hours"""
    import logging
    logger = logging.getLogger(__name__)
    def delayed_delete():
        time.sleep(delay_hours * 3600)  # Convert hours to seconds
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Auto-deleted file: {file_path}")
        except FileNotFoundError:
            logger.warning(f"File not found for auto-delete: {file_path}")
        except Exception as e:
            logger.error(f"Error auto-deleting file {file_path}: {e}")
    thread = threading.Thread(target=delayed_delete)
    thread.daemon = True
    thread.start()

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
            download_record, created = DownloadRequest.objects.get_or_create(
                url=url,
                format="mp4",
                video_id=video_id,
                defaults={'filename': filename}
            )
            
            file_path = os.path.join(output_dir, filename)
            
            # Set up automatic cleanup: always 24 hours
            if settings.AUTO_CLEANUP_ENABLED:
                delete_file_after_delay(file_path, settings.CLEANUP_DOWNLOADS_AFTER_HOURS)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        file_url = f"{request.scheme}://{request.get_host()}/media/downloads/{filename}"
        
        # Always inform user of 24-hour cleanup
        cleanup_info = {
            "message": f"File will be auto-deleted in {settings.CLEANUP_DOWNLOADS_AFTER_HOURS} hours"
        }
        return Response({
            "download_url": file_url,
            "filename": filename,
            "cleanup_info": cleanup_info
        })

# View to manually trigger cleanup
class CleanupView(APIView):
    def post(self, request):
        action = request.data.get("action", "old")  # 'old', 'all', 'orphaned'
        days = request.data.get("days", 2)
        
        output_dir = os.path.join(settings.MEDIA_ROOT, "downloads")
        if not os.path.exists(output_dir):
            return Response({"message": "No downloads directory found"})
        
        count = 0
        space_freed = 0
        
        try:
            if action == "all":
                # Delete all files and records
                import glob
                DownloadRequest.objects.all().delete()
                pattern = os.path.join(output_dir, '*')
                for file_path in glob.glob(pattern):
                    if os.path.isfile(file_path):
                        try:
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            space_freed += file_size
                            count += 1
                        except Exception:
                            pass
                            
            elif action == "orphaned":
                # Delete files without database records
                import glob
                db_filenames = set(DownloadRequest.objects.values_list('filename', flat=True))
                pattern = os.path.join(output_dir, '*')
                for file_path in glob.glob(pattern):
                    if os.path.isfile(file_path):
                        filename = os.path.basename(file_path)
                        if filename not in db_filenames:
                            try:
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                space_freed += file_size
                                count += 1
                            except Exception:
                                pass
                                
            else:  # action == "old"
                # Delete old files based on days
                from datetime import timedelta
                from django.utils import timezone
                
                cutoff = timezone.now() - timedelta(days=days)
                old_downloads = DownloadRequest.objects.filter(created_at__lt=cutoff)
                
                for download in old_downloads:
                    file_path = os.path.join(output_dir, download.filename)
                    try:
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            space_freed += file_size
                            count += 1
                    except Exception:
                        pass
                    download.delete()
            
            space_mb = space_freed / (1024 * 1024)
            return Response({
                "success": True,
                "files_deleted": count,
                "space_freed_mb": round(space_mb, 2),
                "action": action
            })
            
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=500)
