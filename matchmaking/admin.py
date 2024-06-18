"""Deals admin page."""
from django.contrib import admin

from matchmaking.models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """Admin for Deal model."""

    list_display = [
        "id",
        "status",
        "bull_profile",
        "bear_profile",
        "token",
        "deal_amount",
        "open_price",
        "close_price",
        "open_at",
        "close_at",
    ]
    search_fields = ["token"]
