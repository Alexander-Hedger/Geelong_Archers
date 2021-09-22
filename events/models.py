from django.db import models
from django.utils import timezone
import uuid


class EventIntro(models.Model):
    title = models.CharField(max_length=140)
    short_title = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=250)
    max_participants = models.IntegerField(blank=True, null=True)
    current_participants = models.IntegerField(default=0)
    min_age = models.IntegerField(default=10)
    photo = models.ImageField(upload_to='photos/events', blank=True)
    is_published = models.BooleanField(default=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return self.short_title


class EventMotD(models.Model):
    short_title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='photos/events', blank=True)
    is_published = models.BooleanField(default=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def __str__(self):
        return self.short_title


class EventComp(models.Model):
    title = models.CharField(max_length=140)
    short_title = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=250)
    max_participants = models.IntegerField(blank=True, null=True)
    current_participants = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='photos/events', blank=True)
    is_published = models.BooleanField(default=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    event_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.short_title
