"""Tokens admin page."""
from django.contrib import admin

from tokens.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    """Admin for Token model."""

    list_display = [
        "id",
        "token",
        "price",
        "modified_at",
    ]
    search_fields = ["token"]
