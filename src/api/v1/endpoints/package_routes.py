import asyncio

from fastapi import APIRouter, Body, Cookie, Query
from loguru import logger
from src.application.queries.get_package import get_package_query
from src.application.queries.list_packages import list_packages_query
from src.exceptions import PackageRegistrationFailedHTTPException, NoAccessTokenHTTPException
from src.infrastructure.dependencies import DBDep, PaginationDep
from src.shared.schemas.package_schemas import PackageCreateRequest, PackageResponse
from src.infrastructure.tasks.tasks import register_package_task

router = APIRouter(prefix="/packages", tags=["Посылки"])


@router.get("/my_packages", summary="Получить список своих посылок")
async def get_packages(
    pagination: PaginationDep,
    db: DBDep,
    session_id: str = Cookie(default=None),
    type_id: int | None = Query(default=None),
    has_delivery_cost: bool | None = Query(default=None),
):

    logger.info(
        f"Получен запрос списка посылок: session_id={session_id}, "
        f"pagination={pagination}, type_id={type_id}, has_delivery_cost={has_delivery_cost}"
    )

    if not session_id:
        logger.warning("Попытка доступа к /my_packages без session_id")
        raise NoAccessTokenHTTPException

    try:

        result =  await list_packages_query(
            db=db,
            session_id=session_id,
            pagination=pagination,
            type_id=type_id,
            has_delivery_cost=has_delivery_cost,
        )

        logger.info(f"Результат запроса: {result}")

        return result

    except Exception as e:
        logger.error(f"Ошибка при обработке запроса /my_packages: {e}")
        raise

@router.get(
    "/{package_id}",
    response_model=PackageResponse,
    summary="Данные посылки",
    description="Получение данных о посылке по ID (Retrieve package data by ID)"
)
async def get_package(package_id: int, db: DBDep, session_id: str = Cookie(None)):

    if not session_id:
        raise NoAccessTokenHTTPException

    return await get_package_query(db=db, package_id=package_id, session_id=session_id)


@router.post("", response_model=dict, summary="Отправка посылки")
async def create_package(package_data: PackageCreateRequest = Body(openapi_examples={
                            "1": {
                                "summary": "Малый короб",
                                "value": {
                                    "name": "Малый короб",
                                    "weight": 0.5,
                                    "type_id": 1,
                                    "content_value": 100,
                                }
                            },
                            "2": {
                                "summary": "Средний короб",
                                "value": {
                                    "name": "Средний короб",
                                    "weight": 1.5,
                                    "type_id": 2,
                                    "content_value": 200,
                                }
                            },
                            "3": {
                                "summary": "Большой короб",
                                "value": {
                                    "name": "Большой короб",
                                    "weight": 4,
                                    "type_id": 3,
                                    "content_value": 500,
                                }
                            }
                        }),
                         session_id: str = Cookie(default=None),
                        ):
    logger.debug(f"[create_package] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")
    try:
        logger.info(f"Полученные данные посылки: {package_data}")
        logger.info(f"ID сессии: {session_id}")
        # Отправляем задачу на выполнение в Celery
        task = register_package_task.apply_async(args=[package_data.model_dump(), session_id], queue='celery')

        # Ожидание результата задачи
        result = task.get(timeout=10)

        if "package_id" not in result:
            logger.error("Ошибка в результате выполнения задачи Celery: package_id not found")
            raise ValueError("Ошибка в результате выполнения задачи Celery.")

        logger.info(f"Посылка успешно зарегистрирована с ID: {result['package_id']}")
        return {"status": "success", "package_id": result["package_id"]}

    except Exception as e:
        logger.error(f"Ошибка в create_package: {str(e)}")
        # Общая обработка ошибок
        raise PackageRegistrationFailedHTTPException

