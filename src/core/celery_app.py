from celery import Celery

from src.core.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.infrastructure.tasks.celery_tasks"
    ],
)
