from indel.celery import app
from tokens.coingecko_client import CoingeckoClient
from tokens.usecases.store_token_price import TokenPriceStorageUsecase


@app.task()
def store_token_price() -> None:
    """Store token prices."""
    usecase = TokenPriceStorageUsecase(client=CoingeckoClient())
    usecase.store_token_prices()
