from fastapi import APIRouter, Body

from src.exceptions import ObjectAlreadyExistsException, ObjectAlreadyExistsHTTPException
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
    return await db.type.get_all()


@router.post("", response_model=TypeResponse, summary="Создание типа посылки")
async def create_type(db: DBDep, type_data: TypeCreate = Body(openapi_examples={
    "1": {
        "summary": "одежда",
        "value": {
            "name": "одежда",
        }
    },
    "2": {
        "summary": "электроника",
        "value": {
            "name": "электроника",
        }
    },
    "3": {
        "summary": "разное",
        "value": {
            "name": "разное",
        }
    }
    })):

    try:
        package_type = await db.type.create(type_data)
    except Exception:
        raise ObjectAlreadyExistsHTTPException
    await db.commit()
    return package_type
