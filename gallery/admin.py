from django.contrib import admin
from .models import Image, Album


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'thumbnail', 'album', 'position')
    search_fields = ('image', 'album')
    list_per_page = 25


admin.site.register(Image, ImageAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'feature_image', 'quantity',
                    'date_published', 'date_updated')
    search_fields = ('title',)
    list_per_page = 25


admin.site.register(Album, AlbumAdmin)
