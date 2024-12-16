from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import insert
from src.domain.models import PackageOrm
from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.repositories.mappers import PackageDataMapper


class PackageRepository(BaseRepository):
    model = PackageOrm
    mapper = PackageDataMapper

    async def create_with_type(self, session, package_data):
        """
        Создать пакет и одновременно получить связанные данные из таблицы package_types.
        """

        query = (
            insert(self.model)
            .values(**package_data.dict(exclude={'id'}))    # Исключаем поле id
            .returning(self.model.id)   # Возвращаем только id для дальнейшего запроса
        )
        result = await session.execute(query)

        created_package = result.scalar_one()

        # Выполнить подгрузку связанных данных
        query_with_type = (
            select(self.model)
            .options(joinedload(PackageOrm.package_type))
            .filter(PackageOrm.id == created_package.id)
        )
        result_with_type = await session.execute(query_with_type)

        return result_with_type.scalar_one()
