from django.contrib import admin
from .models import CommitteeMinutes, AgmMinutes


# Register your models here

class CommitteeMinutesAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'date_updated')
    search_fields = ('title', 'date_published', 'date_updated')
    readonly_fields = ('date_published',)
    list_per_page = 25


admin.site.register(CommitteeMinutes, CommitteeMinutesAdmin)


class AgmMinutesAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'date_updated')
    search_fields = ('title', 'date_published', 'date_updated')
    readonly_fields = ('date_published',)
    list_per_page = 25


admin.site.register(AgmMinutes, AgmMinutesAdmin)
