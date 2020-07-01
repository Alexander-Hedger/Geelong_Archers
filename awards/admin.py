from django.contrib import admin
from .models import MemberEvents, Awards, MemberAwards, MemberAvailableAwards, MemberClassification, MemberClassificationAnnual

# Register your models here.


class AwardsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 25
    search_fields = ('name',)


admin.site.register(Awards, AwardsAdmin)


class MemberEventsAdmin(admin.ModelAdmin):
    list_display = ('member', 'event_name', 'date')
    list_per_page = 25
    search_fields = ('member', 'event_name', 'date')


admin.site.register(MemberEvents, MemberEventsAdmin)


class MemberAwardsAdmin(admin.ModelAdmin):
    list_display = ('member', 'award', 'date_recieved')
    list_per_page = 25
    search_fields = ('member', 'award', 'date_recieved')


admin.site.register(MemberAwards, MemberAwardsAdmin)


class MemberAvailableAwardsAdmin(admin.ModelAdmin):
    list_display = ('member', 'award')
    list_per_page = 25
    search_fields = ('member', 'award')


admin.site.register(MemberAvailableAwards, MemberAvailableAwardsAdmin)


class MemberClassificationAdmin(admin.ModelAdmin):
    list_display = ('member', 'name', 'score_count')
    list_per_page = 25
    search_fields = ('member', 'name', 'score_count')


admin.site.register(MemberClassification, MemberClassificationAdmin)


class MemberClassificationAnnualAdmin(admin.ModelAdmin):
    list_display = ('member', 'name', 'score_count')
    list_per_page = 25
    search_fields = ('member', 'name', 'score_count')


admin.site.register(MemberClassificationAnnual,
                    MemberClassificationAnnualAdmin)
