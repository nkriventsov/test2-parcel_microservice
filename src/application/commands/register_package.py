from loguru import logger
from src.infrastructure.db.db_manager import DBManager
from src.infrastructure.db.database import async_session_maker
from src.infrastructure.connectors.init import redis_manager
from src.domain.services.cost_calculator import calculate_delivery_cost
from src.shared.schemas.package_schemas import PackageCreateRequest, PackageCreate


async def register_package_command(package_data: dict, session_id: str):
    """
    Команда для регистрации посылки:
    1. Валидирует входные данные.
    2. Получает курс валют из Redis.
    3. Рассчитывает стоимость доставки.
    4. Сохраняет данные в БД.
    """

    logger.info(f"Начата регистрация посылки с данными: {package_data}, session_id: {session_id}")

    try:
        # Валидация данных через Pydantic
        validated_data = PackageCreateRequest(**package_data)

        # Подключение к Redis
        await redis_manager.connect()

        # Получение курса валют
        exchange_rate = await redis_manager.get("rub_to_usd")

        if not exchange_rate:
            raise ValueError("Курс валют отсутствует!")

        # Расчет стоимости доставки
        cost = calculate_delivery_cost(
            weight=validated_data.weight,
            value=validated_data.content_value,
            rate=float(exchange_rate),
        )

        logger.info(f"Стоимость доставки рассчитана: {cost}")

        # Сохранение данных о посылке в PostgreSQL
        async with DBManager(session_factory=async_session_maker) as db:
            package: PackageCreate = await db.package.create(
                PackageCreate(
                    name=validated_data.name,
                    weight=validated_data.weight,
                    type_id=validated_data.type_id,
                    content_value=validated_data.content_value,
                    delivery_cost=cost,
                    session_id=session_id,
                )
            )

        logger.info(f"Посылка зарегистрирована с расчетной стоимостью: {cost}")

        return {"status": "success", "delivery_cost": cost, "package_id": package.id}

    except Exception as e:
        logger.error(f"Ошибка при регистрации посылки: {e}")
        raise
