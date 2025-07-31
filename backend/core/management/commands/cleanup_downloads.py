import os
import glob
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from core.models import DownloadRequest
from django.conf import settings

class Command(BaseCommand):
    help = 'Deletes downloaded files older than N days (default: 2) and orphaned files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=2,
            help='Delete files older than this many days',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Delete all downloaded files regardless of age',
        )
        parser.add_argument(
            '--orphaned',
            action='store_true',
            help='Only delete orphaned files (files without database records)',
        )

    def handle(self, *args, **options):
        days = options['days']
        delete_all = options['all']
        orphaned_only = options['orphaned']
        downloads_path = os.path.join(settings.MEDIA_ROOT, 'downloads')
        
        if not os.path.exists(downloads_path):
            self.stdout.write(self.style.WARNING("Downloads directory doesn't exist"))
            return

        count = 0
        space_freed = 0

        if orphaned_only:
            count, space_freed = self.cleanup_orphaned_files(downloads_path)
        elif delete_all:
            count, space_freed = self.cleanup_all_files(downloads_path)
        else:
            count, space_freed = self.cleanup_old_files(downloads_path, days)

        space_mb = space_freed / (1024 * 1024)
        self.stdout.write(
            self.style.SUCCESS(
                f"Cleanup complete. {count} file(s) deleted. "
                f"Space freed: {space_mb:.2f} MB"
            )
        )

    def cleanup_old_files(self, downloads_path, days):
        cutoff = timezone.now() - timedelta(days=days)
        qs = DownloadRequest.objects.filter(created_at__lt=cutoff)
        count = 0
        space_freed = 0

        for entry in qs:
            file_path = os.path.join(downloads_path, entry.filename)
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                space_freed += file_size
                count += 1
                self.stdout.write(f"Deleted: {entry.filename}")
            except FileNotFoundError:
                self.stdout.write(f"File not found: {entry.filename}")
            except Exception as e:
                self.stdout.write(f"Error deleting {entry.filename}: {e}")
            entry.delete()

        return count, space_freed

    def cleanup_all_files(self, downloads_path):
        count = 0
        space_freed = 0
        
        # Delete all database records
        DownloadRequest.objects.all().delete()
        
        # Delete all files in downloads directory
        pattern = os.path.join(downloads_path, '*')
        for file_path in glob.glob(pattern):
            if os.path.isfile(file_path):
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    space_freed += file_size
                    count += 1
                    self.stdout.write(f"Deleted: {os.path.basename(file_path)}")
                except Exception as e:
                    self.stdout.write(f"Error deleting {file_path}: {e}")

        return count, space_freed

    def cleanup_orphaned_files(self, downloads_path):
        count = 0
        space_freed = 0
        
        # Get all filenames from database
        db_filenames = set(DownloadRequest.objects.values_list('filename', flat=True))
        
        # Get all files in downloads directory
        pattern = os.path.join(downloads_path, '*')
        for file_path in glob.glob(pattern):
            if os.path.isfile(file_path):
                filename = os.path.basename(file_path)
                if filename not in db_filenames:
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        space_freed += file_size
                        count += 1
                        self.stdout.write(f"Deleted orphaned file: {filename}")
                    except Exception as e:
                        self.stdout.write(f"Error deleting {file_path}: {e}")

        return count, space_freed
