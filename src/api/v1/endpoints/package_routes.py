from fastapi import APIRouter, Body, Cookie, Query, Depends

from src.exceptions import ObjectNotFoundException, PackageNotFoundHTTPException
from src.infrastructure.dependencies import DBDep, PaginationDep, PaginationParams
from src.shared.schemas.package_schemas import PackageCreateRequest, PackageResponse, PackageUpdate, PackageCreate

router = APIRouter(prefix="/packages", tags=["Посылки"])


@router.get(
    "/{package_id}",
    response_model=PackageResponse,
    summary="Данные посылки",
    description="Получение данных о посылке по ID (Retrieve package data by ID)"
)
async def get_package(package_id: int, db: DBDep):
    try:
        return await db.package.get_one(package_id)
    except Exception:
        raise PackageNotFoundHTTPException


@router.get("/my_packages", summary="Получить список своих посылок")
async def get_packages(
    db: DBDep,
    session_id: str = Cookie(default=None),
    type_id: int | None = Query(default=None),
    has_delivery_cost: bool | None = Query(default=None),
    pagination: PaginationParams = Depends(PaginationDep),
):
    packages = await db.package.get_filtered(
        session_id=session_id,
        type_id=type_id,
        has_delivery_cost=has_delivery_cost,
        limit=pagination.per_page,
        offset=(pagination.page - 1) * pagination.per_page,
    )
    return packages


@router.post("", response_model=PackageResponse, summary="Отправка посылки")
async def create_package(db: DBDep, package_data: PackageCreateRequest = Body(openapi_examples={
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
    })):

    package = await db.package.create(package_data)
    await db.commit()
    return package
