from typing import TypeVar, Type

from pydantic import BaseModel

from src.infrastructure.db.database import Base

# Общие переменные типов для модели базы данных и схемы
DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Type[DBModelType] = None  # Тип модели базы данных
    schema: Type[SchemaType] = None  # Тип схемы Pydantic

    @classmethod
    def map_to_domain_entity(cls, data: DBModelType) -> SchemaType:
        """
        Преобразует экземпляр модели базы данных в доменную сущность (схему Pydantic).

        Аргументы:
            data (DBModelType): Экземпляр модели базы данных.

        Возвращает:
            SchemaType: Соответствующий экземпляр схемы Pydantic.
        """
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: SchemaType) -> DBModelType:
        """
        Преобразует доменную сущность (схему Pydantic) в экземпляр модели базы данных.

        Аргументы:
            data (SchemaType): Экземпляр схемы Pydantic.

        Возвращает:
            DBModelType: Соответствующий экземпляр модели базы данных.
        """
        return cls.db_model(**data.model_dump())
