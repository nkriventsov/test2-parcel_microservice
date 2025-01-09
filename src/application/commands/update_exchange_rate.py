from loguru import logger
from src.infrastructure.connectors.init import redis_manager
from src.infrastructure.external.currency_service import fetch_exchange_rate


async def update_exchange_rate_command():
    """
    Периодическая задача обновления курса валют в Redis.
    """

    logger.info("Начало обновления курса валют.")

    try:
        await redis_manager.connect()

        rate = await fetch_exchange_rate(redis_manager)
        logger.info(f"Курс валют успешно получен: {rate}")

        await redis_manager.set("rub_to_usd", rate, expire=3600)
        logger.info(f"Курс валют обновлен: {rate}")

        return {"status": "updated", "rate": rate}

    except Exception as e:
        logger.error(f"Ошибка при обновлении курса валют: {e}")
        raise
