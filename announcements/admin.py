from django.contrib import admin
from .models import Announcement


# Register your models here

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'is_published', 'date_published')
    search_fields = ('title', 'short_title', 'date_published',)
    list_editable = ('is_published',)
    readonly_fields = ('date_published',)
    list_per_page = 25


admin.site.register(Announcement, AnnouncementAdmin)
