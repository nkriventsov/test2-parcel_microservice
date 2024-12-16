from celery import Celery
from src.core.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.RABBITMQ_URL,
    backend=settings.CELERY_DB_URL,
    include=["src.infrastructure.tasks.tasks"]
)


# Настройка периодических задач (если потребуется в будущем)
celery_instance.conf.beat_schedule = {
    "update_exchange_rate_every_hour": {
        "task": "src.infrastructure.tasks.tasks.update_exchange_rate",
        "schedule": 3600.0,  # Каждые 3600 секунд (1 час)
    },
}
