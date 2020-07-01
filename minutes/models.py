import os

from django.db import models
from django.utils import timezone
from django.dispatch import receiver

# Create your models here.


class CommitteeMinutes(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now, blank=True)
    date_published = models.DateTimeField(default=timezone.now, blank=True)
    date_updated = models.DateTimeField(default=timezone.now, blank=True)
    minutes = models.FileField(upload_to='docs/committee_minutes/%Y')

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=CommitteeMinutes)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.minutes:
        if os.path.isfile(instance.minutes.path):
            os.remove(instance.minutes.path)


@receiver(models.signals.pre_save, sender=CommitteeMinutes)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).minutes
    except sender.DoesNotExist:
        return False

    new_file = instance.minutes
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class AgmMinutes(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now, blank=True)
    date_published = models.DateTimeField(default=timezone.now, blank=True)
    date_updated = models.DateTimeField(default=timezone.now, blank=True)
    minutes = models.FileField(upload_to='docs/agm_minutes/%Y')

    def __str__(self):
        return self.title
