from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + ((None, {'fields': ('role', 'workspace_id', 'api_rate_limit')}),)
    list_display = ('username', 'email', 'role', 'workspace_id', 'is_staff')
    search_fields = ('username', 'email', 'workspace_id')
