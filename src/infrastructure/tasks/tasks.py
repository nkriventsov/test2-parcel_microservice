import asyncio
from loguru import logger
from asgiref.sync import async_to_sync

from src.application.commands.register_package import register_package_command
from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.core.celery_app import celery_instance
from src.core.config import settings
from src.domain.models import PackageOrm
from src.infrastructure.connectors.redis_connector import RedisManager


@celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
async def register_package_task(package_data: dict, session_id: str):
    """
    Синхронная обертка для асинхронного вызова register_package_command - Вариант 2
    """
    logger.debug(f"[register_package_task] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")

    try:
        logger.info(f"Начало задачи с данными посылки: {package_data}, session_id: {session_id}")

        redis_manager = RedisManager(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )


        # Вызов асинхронной команды через async_to_sync
        result = async_to_sync(register_package_command)(
            package_data=package_data,
            session_id=session_id,
            redis_manager=redis_manager,
        )

        logger.info(f"Посылка успешно зарегистрирована: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
        raise



@celery_instance.task(name="src.infrastructure.tasks.tasks.update_exchange_rate")
def update_exchange_rate_task():
    """
    Синхронная задача для обновления курса валют.
    """
    try:

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        loop.run_until_complete(update_exchange_rate_command())

    except Exception as e:
        logger.error(f"Ошибка обновления курса валют: {e}")
        raise

    finally:
        loop.close()
