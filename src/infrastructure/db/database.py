from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


# Фабрика для создания `async_session_maker`
def get_session_maker():
    engine = create_async_engine(settings.DB_URL, echo=True)
    return async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


