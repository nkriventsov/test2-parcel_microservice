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

# Настройки логирования Celery
celery_instance.conf.update(
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] Task %(task_name)s[%(task_id)s] - %(message)s",
    worker_redirect_stdouts_level="DEBUG",  # Уровень логирования
)

# # Настройка пула и режима выполнения задач
celery_instance.conf.task_always_eager = False
celery_instance.conf.worker_pool = "gevent"   # Используем gevent для асинхронного выполнения


# Настройка периодических задач (если потребуется в будущем)
celery_instance.conf.beat_schedule = {
    "update_exchange_rate_every_hour": {
        "task": "src.infrastructure.tasks.tasks.update_exchange_rate",
        "schedule": 3600.0,  # Каждые 3600 секунд (1 час)
    },
}
