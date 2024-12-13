from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from typing import List, Optional, Type
from sqlalchemy.exc import NoResultFound

from src.exceptions import ObjectNotFoundException
from src.infrastructure.repositories.mappers.base import DataMapper


class BaseRepository:
    model: Type[BaseModel] = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, limit=None, offset=None, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)

        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

    async def create(self, domain_entity: BaseModel) -> BaseModel:
        db_entity = self.mapper.map_to_persistence_entity(domain_entity)
        self.session.add(db_entity)
        await self.session.commit()
        await self.session.refresh(db_entity)
        return self.mapper.map_to_domain_entity(db_entity)

    async def update(self, entity_id: int, domain_entity: BaseModel) -> Optional[BaseModel]:
        db_entity = await self.get_by_id(entity_id)
        if not db_entity:
            return None
        updated_entity = self.mapper.map_to_persistence_entity(domain_entity)
        for key, value in updated_entity.items():
            setattr(db_entity, key, value)
        await self.session.commit()
        await self.session.refresh(db_entity)
        return self.mapper.map_to_domain_entity(db_entity)

    async def delete(self, entity_id: int) -> bool:
        query = delete(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0
