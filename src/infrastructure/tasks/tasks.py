import asyncio
from loguru import logger

from src.application.commands.register_package import register_package_command
from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.core.celery_app import celery_instance


@celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
def register_package_task(package_data: dict, session_id: str):

    asyncio.run(register_package_command(package_data, session_id))


@celery_instance.task(name="src.infrastructure.tasks.tasks.update_exchange_rate")
def update_exchange_rate_task():

    asyncio.run(update_exchange_rate_command())
