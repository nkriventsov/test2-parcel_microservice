from loguru import logger

from src.application.commands.update_exchange_rate import update_exchange_rate_command
from src.exceptions import PackageRegistrationFailedHTTPException
from src.infrastructure.connectors.redis_connector import RedisManager
from src.infrastructure.db.db_manager import DBManager
from src.infrastructure.db.database import async_session_maker
from src.domain.services.cost_calculator import calculate_delivery_cost
from src.shared.schemas.package_schemas import PackageCreateRequest, PackageCreate


async def register_package_command(package_data: dict, session_id: str, redis_manager: RedisManager):
    """
    Команда для регистрации посылки:
    1. Валидирует входные данные.
    2. Получает курс валют из Redis.
    3. Рассчитывает стоимость доставки.
    4. Сохраняет данные в БД.
    5. Формирование результата.
    """

    logger.info(f"Начата регистрация посылки с данными: {package_data}, session_id: {session_id}")

    try:
        # Валидация данных через Pydantic
        validated_data = PackageCreateRequest(**package_data)

        # Работа с Redis через контекстный менеджер
        async with redis_manager as redis_conn:

            # Получение курса валют
            exchange_rate = await redis_conn.get("rub_to_usd")

            if not exchange_rate:
                logger.warning("Курс валют отсутствует в Redis. Запуск обновления курса.")
                updated_rate = await update_exchange_rate_command()
                exchange_rate = updated_rate["rate"]

            # Расчет стоимости доставки
            cost = calculate_delivery_cost(
                weight=validated_data.weight,
                content_value=validated_data.content_value,
                exchange_rate=float(exchange_rate),
            )

            logger.info(f"Стоимость доставки рассчитана: {cost}")

        # Сохранение данных о посылке в PostgreSQL
        async with DBManager(session_factory=async_session_maker, redis_manager=redis_manager) as db:
            # Создаём пакет с загрузкой связанных данных
            created_package = await db.package.create_with_type(
                session=db.session,
                package_data=PackageCreate(
                    name=validated_data.name,
                    weight=validated_data.weight,
                    type_id=validated_data.type_id,
                    content_value=validated_data.content_value,
                    delivery_cost=cost,
                    session_id=session_id,
                ),
            )

            await db.commit()

        logger.info(f"Посылка зарегистрирована с расчетной стоимостью: {cost}")

        # Преобразуем ORM-объект в доменную модель до завершения контекста
        package = db.package.mapper.map_to_domain_entity(created_package)

        return {"package_id": package.id}

    except Exception as e:
        logger.error(f"Ошибка при регистрации посылки: {e}")
        raise PackageRegistrationFailedHTTPException
