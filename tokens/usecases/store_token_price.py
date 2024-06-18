"""Usecase for storing token price."""
import dataclasses

from django.conf import settings

from tokens.coingecko_client import CoingeckoClientInterface, BaseCurrencyResponse
from tokens.models import Token


@dataclasses.dataclass
class TokenPriceStorageUsecase:
    """Usecase to store token prices."""

    client: CoingeckoClientInterface

    def store_token_prices(self) -> None:
        """Store token prices."""
        res = self.client.fetch_token_price(tokens=settings.TOKENS_TO_FETCH, currency=settings.CURRENCY)
        self.save_tokens_in_db(res)

    def save_tokens_in_db(self, response: dict[str, BaseCurrencyResponse]) -> None:
        """Overwrite existing tokens data to db."""
        tokens = [Token(token=token, price=currency.usd) for token, currency in response.items()]

        Token.objects.bulk_create(
            tokens,
            update_conflicts=True,
            unique_fields=["token"],
            update_fields=["price", "modified_at"],
        )
