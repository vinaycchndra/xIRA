from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('work_email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('work_email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')

    ordering = ['-date_joined']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('work_email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
