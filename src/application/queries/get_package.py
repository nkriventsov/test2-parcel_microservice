from loguru import logger
from src.exceptions import PackageNotFoundHTTPException
from src.infrastructure.dependencies import DBDep


async def get_package_query(db: DBDep, package_id: int):

    logger.info(f"Запрос получения данных посылки с ID: {package_id}")

    try:
        package = await db.package.get_one(package_id)
        logger.info(f"Данные посылки получены: {package}")

        if not package:
            logger.warning(f"Посылка с ID {package_id} не найдена.")
            raise PackageNotFoundHTTPException

        return package

    except Exception as e:
        logger.error(f"Ошибка при получении данных посылки: {e}")
        raise PackageNotFoundHTTPException
