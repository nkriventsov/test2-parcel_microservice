from celery import Celery

from src.core.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.infrastructure.tasks.tasks"
    ],
)

celery_instance.conf.beat_schedule = {
    "calculate_costs_every_5_minutes": {
        "task": "src.infrastructure.tasks.tasks.calculate_costs",
        "schedule": 300.0,  # каждые 5 минут
    },
}

