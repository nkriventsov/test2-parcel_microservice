from loguru import logger

from src.domain.models import PackageOrm
from src.infrastructure.dependencies import PaginationParams


async def list_packages_query(
    db,
    session_id: str,
    pagination: PaginationParams,
    type_id: int | None = None,
    has_delivery_cost: bool | None = None,
):
    logger.info(f"Запрос списка посылок с фильтрами: session_id={session_id}, "
                f"type_id={type_id}, has_delivery_cost={has_delivery_cost}")

    try:
        filters = [PackageOrm.session_id == session_id]

        if type_id:
            filters.append(PackageOrm.type_id == type_id)
        if has_delivery_cost is not None:
            filters.append(PackageOrm.delivery_cost.is_not(None)
                           if has_delivery_cost
                           else PackageOrm.delivery_cost.is_(None))

        logger.debug(f"Сформированные фильтры: {filters}")

        per_page = pagination.per_page or 5

        packages = await db.package.get_filtered(*filters,
                                                 limit=pagination.per_page,
                                                 offset=(pagination.page - 1) * per_page)

        logger.info(f"Возвращено {len(packages)} посылок.")

        return packages

    except Exception as e:
        logger.error(f"Ошибка при запросе списка посылок: {e}")
        raise
