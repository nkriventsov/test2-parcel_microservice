from loguru import logger
from src.infrastructure.dependencies import DBDep
from src.shared.schemas.type_schemas import TypeResponse


async def get_all_types_query(db: DBDep) -> list[TypeResponse]:
    """
    Запрос для получения списка всех типов посылок.
    :param db: Зависимость базы данных.
    :return: Список типов посылок.
    """

    logger.info("Запущен запрос получения всех типов посылок.")

    try:
        result = await db.type.get_all()

        logger.info(f"Получено {len(result)} типов посылок.")

        return result

    except Exception as e:
        logger.error(f"Ошибка при выполнении запроса типов посылок: {e}")
        raise
