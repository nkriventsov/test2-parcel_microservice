from fastapi import APIRouter, Body, Cookie, Query

from src.application.queries.get_package import get_package_query
from src.application.queries.list_packages import list_packages_query
from src.exceptions import PackageRegistrationFailedHTTPException
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

    return await list_packages_query(
        db=db,
        session_id=session_id,
        pagination=pagination,
        type_id=type_id,
        has_delivery_cost=has_delivery_cost,
    )


@router.get(
    "/{package_id}",
    response_model=PackageResponse,
    summary="Данные посылки",
    description="Получение данных о посылке по ID (Retrieve package data by ID)"
)
async def get_package(package_id: int, db: DBDep):

    return await get_package_query(db=db, package_id=package_id)


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
    try:
        # Отправляем задачу на выполнение в Celery
        task = register_package_task.apply_async(args=[package_data.model_dump(), session_id])

        # Ожидание результата задачи
        result = task.get(timeout=1)

        if "package_id" not in result:
            raise ValueError("Ошибка в результате выполнения задачи Celery.")

        return {"status": "success", "package_id": result["package_id"]}

    except Exception as e:
        # Общая обработка ошибок
        raise PackageRegistrationFailedHTTPException

