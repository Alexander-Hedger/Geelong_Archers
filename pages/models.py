from django.db import models

from django.utils import timezone


class PageContent(models.Model):

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    date_updated = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.title
