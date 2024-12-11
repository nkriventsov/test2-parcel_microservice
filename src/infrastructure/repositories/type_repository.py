from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.infrastructure.db.models import TypeModel


class TypeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[TypeModel]:
        query = select(TypeModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, type_id: int) -> TypeModel:
        query = select(TypeModel).where(TypeModel.id == type_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
