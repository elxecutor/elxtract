import os
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from core.models import DownloadRequest
from django.conf import settings

class Command(BaseCommand):
    help = 'Deletes downloaded files older than N days (default: 2)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=2,
            help='Delete files older than this many days',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff = timezone.now() - timedelta(days=days)
        downloads_path = os.path.join(settings.MEDIA_ROOT, 'downloads')

        qs = DownloadRequest.objects.filter(created_at__lt=cutoff)
        count = 0

        for entry in qs:
            file_path = os.path.join(downloads_path, entry.filename)
            try:
                os.remove(file_path)
                count += 1
                self.stdout.write(f"Deleted: {entry.filename}")
            except FileNotFoundError:
                self.stdout.write(f"File not found: {entry.filename}")
            entry.delete()

        self.stdout.write(self.style.SUCCESS(f"Cleanup complete. {count} file(s) deleted."))
