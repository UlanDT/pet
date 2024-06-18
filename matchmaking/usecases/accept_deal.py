from datetime import timedelta

from rest_framework import status
from rest_framework.exceptions import APIException

from matchmaking.models import Deal
from matchmaking.tasks import process_deal
from users.models import Profile


class AcceptDealUsecase:
    """Accept open deal."""

    def accept(self, deal_id: int, profile: Profile) -> None:
        """Accept open deal by profile."""
        deal = self.valid_deal(deal_id, profile)
        deal.close_at = deal.open_at + timedelta(seconds=deal.duration)
        deal.status = Deal.Status.IN_PROGRESS.value

        if deal.bear_profile is None:
            deal.bear_profile = profile
        if deal.bull_profile is None:
            deal.bull_profile = profile

        deal.save()
        process_deal.apply_async([deal.pk], eta=deal.close_at)

    def valid_deal(self, deal_id: int, profile: Profile) -> Deal:
        """Validate request"""
        deal = Deal.objects.filter(pk=deal_id).first()
        if not deal:
            detail = f"Deal with id {deal_id} not found"
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if deal.bull_profile == profile or deal.bear_profile == profile:
            detail = "Deal should contain both bull and bear"
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        if profile.balance < deal.deal_amount:
            detail = "Insufficient funds"
            raise APIException(detail=detail, code=status.HTTP_400_BAD_REQUEST)

        return deal
