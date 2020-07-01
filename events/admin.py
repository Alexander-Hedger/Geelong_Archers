from django.contrib import admin
from .models import EventIntro, EventComp, EventMotD


# Register your models here

class EventIntroAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'is_published',
                    'date_start', 'date_end',)
    search_fields = ('title', 'short_title',)
    list_editable = ('is_published',)
    list_per_page = 25


admin.site.register(EventIntro, EventIntroAdmin)


class EventCompAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'is_published',
                    'date_start', 'date_end',)
    search_fields = ('title', 'short_title',)
    list_editable = ('is_published',)
    list_per_page = 25


admin.site.register(EventComp, EventCompAdmin)


class EventMotDAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'is_published',
                    'date_start', 'date_end',)
    search_fields = ('title', 'short_title',)
    list_editable = ('is_published',)
    list_per_page = 25


admin.site.register(EventMotD, EventMotDAdmin)
