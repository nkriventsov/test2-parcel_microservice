import asyncio

from loguru import logger
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import insert
from sqlalchemy.inspection import inspect
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
        logger.debug(f"[create_with_type] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")
        try:
            logger.debug(f"[create_with_type] Входные данные package_data: {package_data}")

            # Вставляем запись и возвращаем только id
            query = (
                insert(self.model)
                .values(**package_data.dict(exclude={'id'}))    # Исключаем поле id
                .returning(self.model.id)   # Возвращаем только id для дальнейшего запроса
            )
            result = await session.execute(query)

            created_package_id = result.scalar_one()

            # Извлекаем полный объект ORM с подгруженными связанными данными
            query_with_type = (
                select(self.model)
                .options(joinedload(PackageOrm.package_type))  # Подгружаем связанные данные
                .filter(PackageOrm.id == created_package_id)  # Фильтр по созданному id
            )
            result_with_type = await session.execute(query_with_type)

            package_with_type = result_with_type.scalars().first()

            logger.debug(f"[create_with_type] Результат ORM-запроса: {package_with_type}")

            # Трансформация ORM-объекта в словарь
            package_dict = {c.key: getattr(package_with_type, c.key) for c in
                            inspect(package_with_type).mapper.column_attrs}

            # Добавляем связанные данные вручную
            package_dict['type_name'] = package_with_type.package_type.name if package_with_type.package_type else None

            logger.debug(f"[create_with_type] Преобразованный package_dict: {package_dict}")

            return package_dict

        except Exception as e:
            logger.error(f"[create_with_type] Ошибка: {e}")
            raise
