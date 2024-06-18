from indel.celery import app
from matchmaking.usecases.process_deal import ProcessDealUsecase


@app.task()
def process_deal(deal_id: int) -> None:
    """Handle deal."""
    usecase = ProcessDealUsecase()
    usecase.close_deal(deal_id)
