"""Module containing django models for users."""
from __future__ import annotations


from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """User profiles."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_address = models.CharField(max_length=128, null=True, blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self) -> str:
        return f"{self.user.email} at {self.public_address}"
