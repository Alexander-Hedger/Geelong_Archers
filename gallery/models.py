from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Image Compression
import os
from io import BytesIO
from django.core.files import File
from PIL import Image as PILImg
from django.core.files.uploadedfile import InMemoryUploadedFile


def compress(image):
    im = PILImg.open(image)
    im.convert('RGB')
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=80)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


def thumbnail_image(image):
    # Define thumbnail size
    size_300 = (300, 300)
    im = PILImg.open(image)
    im.convert('RGB')
    # create a BytesIO object
    im_io = BytesIO()
    im.thumbnail(size_300)
    # save image to BytesIO object
    im.save(im_io, 'JPEG', quality=70)
    # create a django-friendly Files object
    thumbnail = File(im_io, name=image.name)
    return thumbnail


class Image(models.Model):
    album = models.ForeignKey(
        'Album', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='photos/albums/')
    thumbnail = models.ImageField(
        upload_to='photos/albums/thumbnails', blank=True, null=True)
    position = models.IntegerField()

    def name(self):
        return os.path.basename(self.image.name)

    def __str__(self):
        return os.path.basename(self.image.name)

    def save(self, *args, **kwargs):
        if self.image:
            # call the compress function
            new_image = compress(self.image)
            # Create thumbnail
            thumbnail = thumbnail_image(self.image)
            # set self.image to new_image
            self.image = new_image
            self.thumbnail = thumbnail
            # save
        super().save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Album(models.Model):
    title = models.CharField(max_length=100)
    feature_image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, related_name='feature', blank=True, null=True)
    images = models.ManyToManyField(
        Image, related_name='images', blank=True)
    quantity = models.IntegerField()
    hidden = models.BooleanField(default=False)
    date_published = models.DateTimeField(default=timezone.now, blank=True)
    date_updated = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.title
