from django.contrib import admin
from .models import PageContent
# Register your models here.


class PageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_updated')
    search_fields = ('title',)
    list_per_page = 25


admin.site.register(PageContent, PageContentAdmin)
