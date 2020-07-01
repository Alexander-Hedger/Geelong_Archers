from django.contrib import admin
from .models import ContactIntro
# Register your models here.


class ContactIntroAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'first_name', 'last_name',
                    'age', 'shot_before', 'reason', 'contact_date')
    search_fields = ('event_id', 'first_name', 'last_name')
    list_per_page = 25


admin.site.register(ContactIntro, ContactIntroAdmin)
