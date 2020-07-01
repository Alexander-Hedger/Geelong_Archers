from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    title = models.CharField(max_length=140)
    short_title = models.CharField(max_length=50)
    announcement = models.TextField()
    short_announcement = models.CharField(max_length=250)
    is_published = models.BooleanField(default=True)
    date_published = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.short_title
