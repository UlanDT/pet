from typing import TypedDict
from datetime import datetime, timezone
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from matchmaking.constants import MINIMUM_DEAL_AMOUNT, MINIMUM_DEAL_DURATION
from matchmaking.models import Deal
from tokens.models import Token
from users.models import Profile


class DealCreateDict(TypedDict):
    """Annotate Create deal request data."""

    bull_profile: Profile
    bear_profile: Profile
    token: Token
    deal_amount: int
    duration: int


class ListDealSerializer(serializers.ModelSerializer):
    """Serialize deals list."""

    class Meta:
        """Meta class."""

        model = Deal
        fields = (
            "id",
            "bull_profile",
            "bear_profile",
            "token",
            "deal_amount",
            "duration",
            "status",
            "open_price",
            "close_price",
            "open_at",
            "close_at",
        )


class CreateDealSerializer(serializers.ModelSerializer):
    """Serialize Deal when creating instance."""

    class Meta:
        """Meta class."""

        model = Deal
        fields = ("bull_profile", "bear_profile", "token", "deal_amount", "duration")
        extra_kwargs = {"bull_profile": {"required": False}, "bear_profile": {"required": False}}

    def create(self, validated_data: DealCreateDict) -> Deal:
        """Customize Deal create logic."""
        token = Token.objects.get(token=validated_data["token"])

        open_at = datetime.now(tz=timezone.utc)

        deal = Deal.objects.create(open_price=token.price, open_at=open_at, **validated_data)
        return deal

    def validate(self, data: DealCreateDict) -> DealCreateDict:
        """Validate."""
        token_exists = Token.objects.filter(token=data["token"]).exists()
        if not token_exists:
            detail = "Requested token does not exist."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if data["deal_amount"] < MINIMUM_DEAL_AMOUNT:
            detail = f"Deal amount should not be less than {MINIMUM_DEAL_AMOUNT}."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if data["duration"] < MINIMUM_DEAL_DURATION:
            detail = f"Deal duration should not be less than {MINIMUM_DEAL_DURATION}."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        bull_profile = data.get("bull_profile", None)
        bear_profile = data.get("bear_profile", None)

        if bull_profile is not None and bear_profile is not None:
            detail = "One of bull_profile or bear_profile should be empty when opening a deal."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if bull_profile is None and bear_profile is None:
            detail = "One of bull_profile or bear_profile should exist when opening a deal."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if bull_profile and bull_profile.balance < data["deal_amount"]:
            detail = "Insufficient funds."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if bear_profile and bear_profile.balance < data["deal_amount"]:
            detail = "Insufficient funds."
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        return data
