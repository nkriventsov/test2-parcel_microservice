from celery import Celery
from src.core.config import settings


celery_instance = Celery(
    "tasks",
    broker=settings.RABBITMQ_URL,
    backend=settings.CELERY_DB_URL,
    include=["src.infrastructure.tasks.tasks"]
)

celery_instance.conf.update(
    broker_connection_retry_on_startup=True,
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
)

# Настройка периодических задач (если потребуется в будущем)
celery_instance.conf.beat_schedule = {
    "update_exchange_rate_every_hour": {
        "task": "src.infrastructure.tasks.tasks.update_exchange_rate",
        "schedule": 10.0,  # Каждые 3600 секунд (1 час)
    },
}
