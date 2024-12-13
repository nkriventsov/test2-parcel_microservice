import aiohttp
import redis.asyncio as redis
import json


async def get_exchange_rate(redis_client: redis.Redis) -> float:
    cached_rate = await redis_client.get("usd_to_rub")
    if cached_rate:
        return float(cached_rate)

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.cbr-xml-daily.ru/daily_json.js") as response:
            data = await response.json()
            usd_rate = data["Valute"]["USD"]["Value"]
            await redis_client.set("usd_to_rub", usd_rate, ex=3600)  # Кэшируем на час
            return usd_rate
