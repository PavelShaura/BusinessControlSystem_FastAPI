from celery import Celery

from src.core.config import settings


celery_app = Celery('tasks', broker=f'pyamqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@{settings.RABBITMQ_HOST}//')

celery_app.autodiscover_tasks(["worker.notify"])

