import asyncio
from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel

from loguru import logger
from src.infrastructure.connectors.init import redis_manager
from src.infrastructure.db.database import get_session_maker
from src.infrastructure.db.db_manager import DBManager


# Параметры для пагинации запросов.
class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Страница")]
    # значение по умолчанию: 3, вводимое значение должно быть больше или равно 1 и меньше 30
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Вывод на страницу")]


PaginationDep = Annotated[PaginationParams, Depends()]


# Определяем функцию для создания экземпляра DBManager с использованием фабрики сессий async_session_maker.
def get_db_manager():
    session_factory = get_session_maker()
    return DBManager(session_factory=session_factory, redis_manager=redis_manager)


# Асинхронная генераторная функция, которая предоставляет экземпляр DBManager в асинхронном контекстном менеджере.
async def get_db():
    logger.debug(f"[get_db] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")
    # Создаем экземпляр DBManager, используя контекстный менеджер,
    # чтобы гарантировать корректное создание и закрытие сессии.
    async with get_db_manager() as db:
        logger.debug(f"[get_db_manager] Цикл событий: ID={id(asyncio.get_running_loop())} | Объект={asyncio.get_running_loop()}")
        # Используем yield, чтобы вернуть объект db (экземпляр DBManager)
        # и затем автоматически закрыть сессию после использования.
        yield db

# Создаем типовую аннотацию DBDep, которая определяет зависимость для FastAPI.
# Используется для передачи экземпляра DBManager через механизм зависимостей (Depends) в маршруты FastAPI.
DBDep = Annotated[DBManager, Depends(get_db)]
