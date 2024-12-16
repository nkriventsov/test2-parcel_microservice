import asyncio
from loguru import logger

from src.application.commands.register_package import register_package_command
from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.core.celery_app import celery_instance
from src.infrastructure.connectors.init import redis_manager


@celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
def register_package_task(package_data: dict, session_id: str):

    try:
        result = asyncio.run(register_package_command(package_data, session_id, redis_manager))

        logger.info(f"Посылка зарегистрирована: {result}")

        return result

    except Exception as e:
        logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
        raise


@celery_instance.task(name="src.infrastructure.tasks.tasks.update_exchange_rate")
def update_exchange_rate_task():
    try:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        loop.run_until_complete(update_exchange_rate_command())

    except Exception as e:
        logger.error(f"Ошибка обновления курса валют: {e}")
        raise

    finally:
        loop.close()
