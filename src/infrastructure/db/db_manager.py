from src.infrastructure.repositories.package_repository import PackageRepository
from src.infrastructure.repositories.type_repository import TypeRepository


# Определяем класс DBManager для управления взаимодействием с базой данных.
class DBManager:
    # Инициализатор класса, который принимает session_factory,
    # используемый для создания сессий взаимодействия с базой данных.
    def __init__(self, session_factory):
        self.session_factory = session_factory

    # Асинхронный метод для входа в контекстный менеджер (использование with ... as ...).
    async def __aenter__(self):
        # Создаем сессию базы данных, используя session_factory.
        self.session = self.session_factory()

        # Создаем экземпляры репозиториев для работы с отелями, комнатами и пользователями, передавая созданную сессию.
        self.package = PackageRepository(self.session)
        self.type = TypeRepository(self.session)

        # Возвращаем экземпляр DBManager, чтобы его можно было использовать внутри контекстного менеджера.
        return self

    # Асинхронный метод для выхода из контекстного менеджера.
    async def __aexit__(self, *args):
        # Откатываем все незавершенные изменения, чтобы база данных не оставалась в непоследовательном состоянии.
        await self.session.rollback()
        # Закрываем сессию после использования, освобождая все ресурсы.
        await self.session.close()

    # Асинхронный метод для фиксации изменений в базе данных.
    async def commit(self):
        await self.session.commit()

