"""Tokens admin page."""
from django.contrib import admin

from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin for Profile model."""

    list_display = [
        "id",
        "public_address",
        "balance",
    ]
    search_fields = ["token"]
