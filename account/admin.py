from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'full_name', 'email', 'phone', 'is_active', 'date_joined',]
    list_filter = ['is_superuser', 'is_active',]
    search_fields = ['id', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-id']