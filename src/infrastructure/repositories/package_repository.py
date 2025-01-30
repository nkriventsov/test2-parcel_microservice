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
                .returning(self.model)   # Возвращаем весь объект ORM
            )
            result = await session.execute(query)

            # Получаем созданный объект
            created_package = result.scalars().first()

            # Подгружаем связанные данные через refresh
            await session.refresh(created_package, ['package_type'])

            logger.debug(f"[create_with_type] Результат ORM-запроса: {created_package}")

            # Трансформация ORM-объекта в словарь
            package_dict = {c.key: getattr(created_package, c.key) for c in
                            inspect(created_package).mapper.column_attrs}

            # Добавляем связанные данные вручную
            package_dict['type_name'] = created_package.package_type.name if created_package.package_type else None

            logger.debug(f"[create_with_type] Преобразованный package_dict: {package_dict}")

            return package_dict

        except Exception as e:
            logger.error(f"[create_with_type] Ошибка: {e}")
            raise
