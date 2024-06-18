import os

from celery import Celery, signature
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "indel.settings.local")

app = Celery("indeal")
app.conf.broker_url = 'redis://localhost:6379'
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs) -> None:
    """Periodic tasks."""
    sender.add_periodic_task(
        crontab(minute="*/1"),  # every 1 minutes
        signature("tokens.tasks.store_token_price"),
        name="Collect and store token prices",
    )
