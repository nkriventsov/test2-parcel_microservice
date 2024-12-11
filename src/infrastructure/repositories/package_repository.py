from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.infrastructure.db.models import PackageModel


class PackageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 10) -> List[PackageModel]:
        query = select(PackageModel).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, package_id: int) -> PackageModel:
        query = select(PackageModel).where(PackageModel.id == package_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, package: PackageModel) -> PackageModel:
        self.session.add(package)
        await self.session.commit()
        await self.session.refresh(package)
        return package