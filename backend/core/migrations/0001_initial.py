# Generated by Django 5.1.6 on 2025-07-30 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('format', models.CharField(default='mp4', max_length=10)),
                ('video_id', models.CharField(max_length=128, unique=True)),
                ('filename', models.CharField(max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
