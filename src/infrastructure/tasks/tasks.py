import asyncio
from loguru import logger

from src.application.commands.register_package import register_package_command
from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.core.celery_app import celery_instance
from src.core.config import settings
from src.domain.models import PackageOrm
from src.infrastructure.connectors.redis_connector import RedisManager


# @celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
# def register_package_task(package_data: dict, session_id: str):
#     """
#     Синхронная обертка для асинхронного вызова register_package_command - Вариант 1
#     """
#     logger.info(f"Запуск задачи с данными посылки: {package_data}, session_id: {session_id}")
#     try:
#
#         logger.info(f"Запуск задачи с данными посылки: {package_data}")
#
#         # Создаем RedisManager для этого цикла
#         redis_manager = RedisManager(
#             host=settings.REDIS_HOST,
#             port=settings.REDIS_PORT,
#         )
#
#         # Запускаем команду регистрации посылки
#         result = asyncio.run(register_package_command(package_data, session_id, redis_manager))
#
#         logger.info(f"Посылка успешно зарегистрирована: {result}")
#
#         return result
#
#     except Exception as e:
#         logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
#         raise


# @celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
# def register_package_task(package_data: dict, session_id: str):
#     """
#     Синхронная обертка для асинхронного вызова register_package_command - Вариант 2
#     """
#     try:
#         logger.info(f"Начало задачи с данными посылки: {package_data}, session_id: {session_id}")
#
#         redis_manager = RedisManager(
#             host=settings.REDIS_HOST,
#             port=settings.REDIS_PORT,
#         )
#
#         # Проверяем, существует ли уже цикл событий
#         try:
#             loop = asyncio.get_event_loop()
#             if loop.is_running():
#                 # Если цикл уже запущен, создаем новый
#                 logger.debug("Цикл событий уже запущен, создаем новый цикл")
#                 loop = asyncio.new_event_loop()
#                 asyncio.set_event_loop(loop)
#         except RuntimeError:
#             # Если цикл не существует, создаем новый
#             logger.debug("Цикл событий не существует, создаем новый цикл")
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#
#         # Запускаем корутину в цикле событий
#         logger.info("Запуск корутины register_package_command")
#         result = loop.run_until_complete(register_package_command(package_data, session_id, redis_manager))
#
#         logger.info(f"Посылка успешно зарегистрирована: {result}")
#         return result
#
#     except Exception as e:
#         logger.error(f"Ошибка в Celery задаче регистрации посылки: {str(e)}")
#         raise
#
#     finally:
#         # Закрываем цикл событий, если он был создан в этой функции
#         try:
#             logger.debug("Закрытие цикла событий")
#             loop.close()
#         except Exception as close_error:
#             logger.warning(f"Ошибка при закрытии цикла событий: {close_error}")


# @celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
# async def register_package_task(package_data: dict, session_id: str):
#     """
#     Асинхронная Celery-задача для регистрации посылки.
#     """
#     try:
#         logger.debug(f"[register_package_task] Входные данные: package_data={package_data}, session_id={session_id}")
#
#         redis_manager = RedisManager(
#             host=settings.REDIS_HOST,
#             port=settings.REDIS_PORT,
#         )
#
#         # Лог до вызова асинхронной функции
#         logger.debug("[register_package_task] Перед вызовом register_package_command")
#
#         # Вызываем асинхронную команду регистрации
#         result = await register_package_command(package_data, session_id, redis_manager)
#         logger.debug(f"[register_package_task] Результат register_package_command: {result}")
#         return result
#
#     except Exception as e:
#         logger.error(f"[register_package_task] Ошибка: {e}")
#         raise


# Синхронный движок для SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.shared.schemas.package_schemas import PackageCreate

sync_engine = create_engine(settings.SYNC_DATABASE_URL)  # Добавьте `SYNC_DATABASE_URL` в конфигурацию
SyncSession = sessionmaker(bind=sync_engine)


@celery_instance.task(name="src.infrastructure.tasks.tasks.register_package")
def register_package_task(package_data: dict, session_id: str):
    """
    Синхронная Celery-задача для регистрации посылки.
    """
    try:
        logger.debug(f"[register_package_task] Входные данные: package_data={package_data}, session_id={session_id}")

        # # Инициализация RedisManager
        # redis_manager = RedisManager(
        #     host=settings.REDIS_HOST,
        #     port=settings.REDIS_PORT,
        # )
        #
        # # Подключение к Redis
        # await redis_manager.connect()
        # logger.debug("[register_package_task] Подключение к Redis для получения курса валют")
        #
        # rub_to_usd_bytes = await redis_manager.get("rub_to_usd")
        #
        # if rub_to_usd_bytes is None:
        #     raise ValueError("Курс валют 'rub_to_usd' отсутствует в Redis")
        #
        # # Преобразование результата из байтов в float
        rub_to_usd = 102.2911
        logger.debug(f"[register_package_task] Курс валют из Redis: rub_to_usd={rub_to_usd}")

        # Расчёт стоимости доставки
        weight = package_data.get("weight", 0)
        delivery_cost = weight * rub_to_usd
        logger.debug(f"[register_package_task] Расчитанная стоимость доставки: delivery_cost={delivery_cost}")

        # Создание записи о посылке
        package = PackageOrm(
            name=package_data["name"],
            weight=package_data["weight"],
            type_id=package_data["type_id"],
            content_value=package_data["content_value"],
            session_id=session_id,
            delivery_cost=delivery_cost,
        )

        # Сохранение данных в PostgreSQL
        logger.debug("[register_package_task] Открытие синхронной сессии базы данных")
        with SyncSession() as session:
            session.add(package)
            session.commit()

            # Обновление объекта после коммита
            session.refresh(package)
            logger.debug("[register_package_task] Данные о посылке сохранены в базе")

        logger.debug(f"[register_package_task] ID зарегистрированной посылки: {package.id}")
        return package.id

    except Exception as e:
        logger.error(f"[register_package_task] Ошибка: {e}")
        raise
    #
    # finally:
    #     # Закрытие подключения к Redis
    #     await redis_manager.close()
    #     logger.debug("[register_package_task] Подключение к Redis закрыто")




# @celery_instance.task(name="src.infrastructure.tasks.tasks.update_exchange_rate")
# def update_exchange_rate_task():
#     """
#     Синхронная задача для обновления курса валют.
#     """
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


@celery_instance.task(name="src.infrastructure.tasks.tasks.update_exchange_rate")
async def update_exchange_rate_task(self):
    """
    Асинхронная задача для обновления курса валют.
    """
    try:
        await update_exchange_rate_command()

    except Exception as e:
        logger.error(f"Ошибка обновления курса валют: {e}")
        raise
