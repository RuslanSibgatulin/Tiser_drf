from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TiserUser


@admin.register(TiserUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username", "email", "first_name", "last_name", "is_staff",
        "amount"
    )
