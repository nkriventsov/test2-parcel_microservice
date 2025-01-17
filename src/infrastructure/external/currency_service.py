import asyncio

import aiohttp
from loguru import logger

from src.exceptions import ObjectNotFoundHTTPException
from src.infrastructure.connectors.redis_connector import RedisManager
from src.core.config import settings
import json


async def fetch_exchange_rate(redis_manager: RedisManager) -> float:
    """Получение курса валют с кэшированием в Redis."""
    logger.debug(f"[fetch_exchange_rate] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")
    # Попытка получить курс валюты из Redis
    cached_rate = await redis_manager.get("rub_to_usd")
    if cached_rate:
        logger.info("Курс валют получен из кэша Redis.")
        return float(cached_rate)

    # Если кэша нет, запрашиваем курс из API
    logger.info("Курс валют отсутствует в кэше, запрос к API...")

    async with aiohttp.ClientSession() as session:
        logger.debug(f"[aiohttp.ClientSession] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")

        async with session.get(settings.CURRENCY_API_HOST) as response:
            logger.debug(f"[session.get(settings.CURRENCY_API_HOST)] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")

            if response.status == 200:
                text = await response.text()  # Получить текстовый контент
                data = json.loads(text)  # Декодировать вручную
                # Извлечь нужное значение
                usd_rate = data["Valute"]["USD"]["Value"]
                logger.info(f"Курс получен с сайта: {usd_rate}")

                # Сохраняем курс валюты в Redis на час
                await redis_manager.set("rub_to_usd", usd_rate, expire=3600)
                logger.info(f"Курс валют записан в Redis: {usd_rate}")
                return usd_rate

            else:
                raise ObjectNotFoundHTTPException

