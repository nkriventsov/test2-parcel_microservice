from fastapi import APIRouter, Body
from loguru import logger

from src.api.v1.endpoints.samples import create_type_sample_data
from src.application.commands.create_package_type import create_type_command
from src.application.queries.get_types import get_all_types_query
from src.infrastructure.dependencies import DBDep
from src.shared.schemas.type_schemas import TypeCreate, TypeResponse

router = APIRouter(prefix="/types", tags=["Типы посылок"])


@router.get(
    "",
    response_model=list[TypeResponse],
    summary="Данные типа посылки",
    description="Получение данных о типах посылкок (Retrieve package type data)"
)
async def get_all_types(db: DBDep):
    """Получить список всех типов посылок."""

    logger.info("Запрос всех типов посылок.")

    result = await get_all_types_query(db)

    logger.info(f"Успешно возвращено {len(result)} типов посылок.")

    return result



@router.post("", response_model=TypeResponse, summary="Создание типа посылки")
async def create_type(db: DBDep, type_data: TypeCreate = Body(openapi_examples=create_type_sample_data)):
    """Создать новый тип посылки."""

    logger.info(f"Создание нового типа посылки: {type_data.model_dump()}")

    result = await create_type_command(db, type_data)

    logger.info(f"Тип посылки успешно создан: {result}")

    return result
