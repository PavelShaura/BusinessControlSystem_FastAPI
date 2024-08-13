from celery import Celery

from src.core.config import settings

celery_app = Celery(
    "celery", backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

celery_app.autodiscover_tasks(["worker.tasks"])
