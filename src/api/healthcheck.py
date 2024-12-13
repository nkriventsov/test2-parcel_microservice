from fastapi import APIRouter, HTTPException, status
from src.domain.models.package import PackageOrm
from sqlalchemy import select

from src.exceptions import DatabaseConnectionHTTPException, DatabaseConnectionException
from src.infrastructure.dependencies import DBDep


healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["Проверка состояния"],
)


@healthcheck_router.get(
    "/",
    summary="Healthcheck",
    description="Проверка состояния приложения",
    response_model=dict,
)
async def healthcheck(db: DBDep):
    try:
        # Проверка подключения к базе данных
        await db.session.execute(select(PackageOrm).limit(1))

        return {"status": "Ok"}

    except DatabaseConnectionException:
        raise DatabaseConnectionHTTPException

