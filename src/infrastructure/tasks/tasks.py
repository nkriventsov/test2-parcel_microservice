import asyncio
from loguru import logger

from src.application.commands.register_package import register_package_command
from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.core.celery_app import celery_instance
from src.core.config import settings
from src.infrastructure.connectors.redis_connector import RedisManager


@celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
# def register_package_task(package_data: dict, session_id: str):
#     """
#     Синхронная обертка для асинхронного вызова register_package_command.
#     """
#
#     try:
#         # Создаем новый event loop для текущего потока
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#
#         # Создаем RedisManager для этого цикла
#         redis_manager = RedisManager(
#             host=settings.REDIS_HOST,
#             port=settings.REDIS_PORT,
#         )
#
#         # Запускаем команду регистрации посылки
#         result = loop.run_until_complete(
#             register_package_command(package_data, session_id, redis_manager)
#         )
#
#         logger.info(f"Посылка зарегистрирована: {result}")
#
#         return result
#
#     except Exception as e:
#         logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
#         raise
#
#     finally:
#         loop.close()
async def register_package_task(self, package_data: dict, session_id: str):
    """
    Асинхронная задача для регистрации посылки.
    """
    try:
        # Создаем RedisManager
        redis_manager = RedisManager(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )

        # Выполняем команду регистрации
        result = await register_package_command(package_data, session_id, redis_manager)

        logger.info(f"Посылка зарегистрирована: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
        raise


@celery_instance.task(name="src.infrastructure.tasks.tasks.update_exchange_rate")
# def update_exchange_rate_task():
#     try:
#
#         loop = asyncio.new_event_loop()
#
#         asyncio.set_event_loop(loop)
#
#         loop.run_until_complete(update_exchange_rate_command())
#
#     except Exception as e:
#         logger.error(f"Ошибка обновления курса валют: {e}")
#         raise
#
#     finally:
#         loop.close()
async def update_exchange_rate_task(self):
    """
    Асинхронная задача для обновления курса валют.
    """
    try:
        await update_exchange_rate_command()

    except Exception as e:
        logger.error(f"Ошибка обновления курса валют: {e}")
        raise
