from loguru import logger

from src.exceptions import ObjectAlreadyExistsHTTPException
from src.infrastructure.dependencies import DBDep
from src.shared.schemas.type_schemas import TypeCreate


async def create_type_command(db: DBDep, type_data: TypeCreate):
    """
    Команда для создания нового типа посылки.
    :param db: Зависимость базы данных.
    :param type_data: Данные типа посылки.
    :return: Созданный тип посылки.
    """

    logger.info(f"Запущена команда создания типа посылки с данными: {type_data.model_dump()}")

    try:
        package_type = await db.type.create(type_data)

        await db.commit()

        logger.info(f"Тип посылки успешно создан: {package_type}")

        return package_type

    except Exception as e:
        logger.error(f"Ошибка создания типа посылки: {e}")
        raise ObjectAlreadyExistsHTTPException



