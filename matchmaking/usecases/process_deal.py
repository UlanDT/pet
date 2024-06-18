from decimal import Decimal

from django.conf import settings
from django.db import transaction

from matchmaking.models import Deal


class ProcessDealUsecase:
    """Process deal."""

    @transaction.atomic
    def close_deal(self, deal_id: int) -> None:
        """Close deal.

        1) Check current token price.
        2) Decide winner.
        3) Redistribute funds accordingly.
        """
        deal = Deal.objects.get(pk=deal_id)

        # If closing price is less than the initial "open_price", bear wins
        if deal.token.price < deal.open_price:
            deal.bear_profile.balance += Decimal(str(deal.deal_amount * settings.DEAL_COEFFICIENT / 100))
            deal.bull_profile.balance -= Decimal(str(deal.deal_amount))

        # If closing price is greater than the initial "open_price", bull wins
        elif deal.token.price > deal.open_price:
            deal.bull_profile.balance += Decimal(str(deal.deal_amount * settings.DEAL_COEFFICIENT / 100))
            deal.bear_profile.balance -= Decimal(str(deal.deal_amount))

        deal.close_price = deal.token.price
        deal.status = Deal.Status.CLOSED.value
        deal.save()
        deal.bear_profile.save()
        deal.bull_profile.save()

        # If closing price is the same as the open price, DRAW
        # This is rare case...
