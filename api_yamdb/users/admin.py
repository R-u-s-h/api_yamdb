from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_superuser",
        "is_staff",
        "last_login",
        "date_joined",
        "email",
    )
    list_editable = (
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_superuser",
        "is_staff",
        "email",
    )
    list_display_links = ("id",)
