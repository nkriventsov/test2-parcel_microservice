from loguru import logger
from src.exceptions import PackageNotFoundHTTPException
from src.infrastructure.dependencies import DBDep


async def get_package_query(db: DBDep, package_id: int, session_id: str):

    logger.info(f"Запрос получения данных посылки с ID: {package_id} и session_id: {session_id}")


    package = await db.package.get_one(id=package_id, session_id=session_id)
    logger.info(f"Данные посылки получены: {package}")

    if not package:
        logger.warning(f"Посылка с ID {package_id} и session_id {session_id} не найдена.")
        raise PackageNotFoundHTTPException

    return package
