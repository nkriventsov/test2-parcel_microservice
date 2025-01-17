import asyncio

from loguru import logger
from src.infrastructure.connectors.redis_connector import RedisManager
from src.infrastructure.repositories.package_repository import PackageRepository
from src.infrastructure.repositories.type_repository import TypeRepository


# Определяем класс DBManager для управления взаимодействием с базой данных.
class DBManager:
    # Инициализатор класса, который принимает session_factory,
    # используемый для создания сессий взаимодействия с базой данных.
    def __init__(self, session_factory, redis_manager: RedisManager):
        self.session_factory = session_factory
        self.redis = redis_manager  # Добавляем менеджер Redis
        logger.debug("DBManager инициализирован с session_factory и redis_manager")

    # Асинхронный метод для входа в контекстный менеджер (использование with ... as ...).
    async def __aenter__(self):
        # Создаем сессию базы данных, используя session_factory.
        logger.debug(f"[DBManager.__aenter__] Цикл событий: {asyncio.get_running_loop()}")
        try:
            self.session = self.session_factory()
            logger.info("Сессия базы данных успешно создана")

            # Создаем экземпляры репозиториев для работы с пакетами и типами, передавая созданную сессию.
            self.package = PackageRepository(self.session)
            self.type = TypeRepository(self.session)
            logger.debug("Репозитории PackageRepository и TypeRepository успешно инициализированы")

            # Возвращаем экземпляр DBManager, чтобы его можно было использовать внутри контекстного менеджера.
            return self
        except Exception as e:
            logger.error(f"Ошибка при инициализации DBManager: {e}")
            raise

    # Асинхронный метод для выхода из контекстного менеджера.
    async def __aexit__(self, *args):
        logger.debug(f"[DBManager.__aexit__] Цикл событий: {asyncio.get_running_loop()}")
        try:
            # Откатываем все незавершенные изменения, чтобы база данных не оставалась в непоследовательном состоянии.
            await self.session.rollback()
            logger.info("Откат изменений в сессии базы данных выполнен")

            # Закрываем сессию после использования, освобождая все ресурсы.
            await self.session.close()
            logger.info("Сессия базы данных успешно закрыта")

        except Exception as e:
            logger.error(f"Ошибка при завершении работы сессии базы данных: {e}")
            raise

    # Асинхронный метод для фиксации изменений в базе данных.
    async def commit(self):
        logger.debug(f"[DBManager.commit] Цикл событий: {asyncio.get_running_loop()}")
        try:
            await self.session.commit()
            logger.info("Изменения в базе данных успешно зафиксированы")
        except Exception as e:
            logger.error(f"Ошибка при фиксации изменений в базе данных: {e}")
            raise

