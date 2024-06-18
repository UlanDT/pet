"""Interact with coingecko API."""
import dataclasses
import json
from typing import Protocol, TYPE_CHECKING

import requests
from django.conf import settings

if TYPE_CHECKING:
    from typing_extensions import Protocol


@dataclasses.dataclass
class BaseCurrencyResponse:
    """Base token response."""

    usd: float


class CoingeckoClientInterface(Protocol):
    """Interface for coingecko client."""

    def fetch_token_price(self, tokens: str, currency: str):
        """Fetch token price."""
        raise NotImplementedError


class CoingeckoClient:
    """Coingecko client methods implementation."""

    def __init__(self):
        self.base_url = settings.COINGECKO_URL

    def fetch_token_price(self, tokens: str, currency: str) -> dict[str: BaseCurrencyResponse]:
        """Fetch token prices.

        :param tokens: List of tokens prices of which should be fetched from API
        :param currency: Name of the currency in which tokens should be converted to (Ex: "usd")
        :return: smth
        """
        url = f"{self.base_url}/simple/price"
        data = requests.get(url, params={"ids": tokens, "vs_currencies": currency})
        content = json.loads(data.content)

        result = {}
        for token, currency_json in content.items():
            result[token] = BaseCurrencyResponse(usd=currency_json["usd"])

        return result
