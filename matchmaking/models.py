"""Module containing deals models."""
from django.db import models

from tokens.models import Token
from users.models import Profile


class Deal(models.Model):
    """Describe model fields here.

    Bull profile: Profile who expects token price to go up
    Bear profile: Profile who expects token price to go down

    Open price: Initial price of token when one of profiles create deal
    Close price: Final price of token when deal got closed (E.g.: open_at + duration)

    ### Example:
    Open price at 12:00 PM for solana is 150 USD with a duration of 300 seconds (5 minutes)
    Close price at 12:05 PM (finish_at) for solana may be 145 USD.
    In this case Bear profile wins because price went down.
    """

    class Status(models.TextChoices):
        """Status choice for status field."""

        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        IN_PROGRESS = "in progress", "In Progress"

    bull_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="bull_deals")
    bear_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="bear_deals")
    token = models.ForeignKey(Token, on_delete=models.PROTECT, related_name="deals")
    deal_amount = models.PositiveIntegerField(default=5)
    duration = models.PositiveIntegerField(default=300)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

    open_price = models.DecimalField(max_digits=20, decimal_places=4, help_text="Price of token when deal got created")
    close_price = models.DecimalField(max_digits=20, decimal_places=4, help_text="Price of token when deal got closed", null=True, blank=True)
    open_at = models.DateTimeField(auto_now_add=True)
    close_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta class."""

        db_table = "deals"

    def __str__(self) -> str:
        return f"{self.deal_amount}$ Deal per {self.token}"
