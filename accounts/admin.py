from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account, Committee, LifeMember


# Register your models here

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'archery_australia_id', 'is_active', 'is_admin')
    list_display_links = ('first_name', 'last_name', 'archery_australia_id')
    search_fields = ('first_name', 'last_name',
                     'archery_australia_id', 'email')
    readonly_fields = ('date_joined', 'last_login')
    list_per_page = 25

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )


admin.site.register(Account, AccountAdmin)


class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('position', 'member', 'email',)


admin.site.register(Committee, CommitteeAdmin)


class LifeMemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'year_made')
    list_per_page = 25
    search_fields = ('first_name', 'last_name')


admin.site.register(LifeMember, LifeMemberAdmin)
