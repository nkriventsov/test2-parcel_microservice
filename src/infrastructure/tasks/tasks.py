import asyncio
from loguru import logger

from src.application.commands.register_package import register_package_command
from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.core.celery_app import celery_instance
from src.core.config import settings
from src.domain.models import PackageOrm
from src.infrastructure.connectors.redis_connector import RedisManager


@celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
def register_package_task(package_data: dict, session_id: str):
    """
    Синхронная обертка для асинхронного вызова register_package_command - Вариант 2
    """
    try:
        logger.info(f"Начало задачи с данными посылки: {package_data}, session_id: {session_id}")

        redis_manager = RedisManager(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )

        # Проверяем, существует ли уже цикл событий
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Если цикл уже запущен, создаем новый
                logger.debug("Цикл событий уже запущен, создаем новый цикл")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
        except RuntimeError:
            # Если цикл не существует, создаем новый
            logger.debug("Цикл событий не существует, создаем новый цикл")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Запускаем корутину в цикле событий
        logger.info("Запуск корутины register_package_command")
        result = loop.run_until_complete(register_package_command(package_data, session_id, redis_manager))

        logger.info(f"Посылка успешно зарегистрирована: {result}")
        return result

    except Exception as e:
        logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
        raise

    finally:
        # Закрываем цикл событий, если он был создан в этой функции
        try:
            logger.debug("Закрытие цикла событий")
            loop.close()
        except Exception as close_error:
            logger.warning(f"Ошибка при закрытии цикла событий: {close_error}")


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
