from django.db import models
from django.utils import timezone
from events.models import EventIntro

# Create your models here.


class ContactIntro(models.Model):
    event_id = models.ForeignKey(
        EventIntro, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    age = models.IntegerField()
    left_right = models.CharField(max_length=10)
    shot_before = models.CharField(max_length=50)
    reason = models.CharField(max_length=15)
    contact_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
