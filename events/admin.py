from django.contrib import admin
from .models import EventIntro, EventComp, EventMotD


# Register your models here

class EventIntroAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'title', 'short_title', 'date_start', 'date_end', 'description',
                    'short_description', 'max_participants', 'current_participants', 'max_lh', 'current_lh',)
    search_fields = ('title', 'short_title',)
    list_editable = ('is_published', 'title', 'short_title', 'date_start', 'date_end', 'description',
                     'short_description', 'max_participants', 'current_participants', 'max_lh', 'current_lh',)
    list_per_page = 25


admin.site.register(EventIntro, EventIntroAdmin)


class EventCompAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'short_title', 'short_description',
                    'date_start', 'date_end',)
    search_fields = ('title', 'short_title',)
    list_editable = ('is_published', 'short_title', 'short_description',
                     'date_start', 'date_end',)
    list_per_page = 25


admin.site.register(EventComp, EventCompAdmin)


class EventMotDAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_published', 'short_title', 'short_description',
                    'date_start', 'date_end',)
    search_fields = ('title', 'short_title',)
    list_editable = ('is_published', 'short_title', 'short_description',
                     'date_start', 'date_end',)
    list_per_page = 25


admin.site.register(EventMotD, EventMotDAdmin)
