import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.api.v1.endpoints.fx_rate_upd import fx_rate
from src.api.v1.endpoints.package_routes import router as package_router
from src.infrastructure.connectors.redis_connector import RedisManager


@pytest.fixture
def test_client():
    """
    Создает тестовый клиент FastAPI для выполнения запросов к API.

    :return: TestClient
    """
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(fx_rate)
    app.include_router(package_router)
    return TestClient(app)


@pytest.fixture
def mock_redis_manager():
    """
    Создает мок-объект для RedisManager, имитирующий подключение к Redis.

    :return: AsyncMock с методами RedisManager
    """
    redis_manager = AsyncMock(spec=RedisManager)
    redis_manager.get.return_value = None  # По умолчанию значение не кэшировано
    redis_manager.set.return_value = None
    redis_manager.connect.return_value = None

    redis_manager.set.side_effect = lambda key, value, expire: print(
        f"Mock redis_manager.set called with key={key}, value={value}, expire={expire}"
    )

    return redis_manager


@pytest.fixture
def mock_fetch_exchange_rate():
    """
    Создает мок-объект для функции fetch_exchange_rate, возвращающий фиксированный курс валюты.

    :return: AsyncMock с фиксированным значением курса
    """
    async_mock = AsyncMock(return_value=75.5)  # Пример курса валюты
    return async_mock


@pytest.fixture
def mock_list_packages_query():
    """
    Создает мок-объект для функции list_packages_query, возвращающий фиктивный список посылок.

    :return: AsyncMock с фиктивным списком посылок
    """
    async_mock = AsyncMock(
        return_value=[
            {
                "id": 1,
                "name": "Малый короб",
                "weight": 0.5,
                "type_id": 1,
                "content_value": 100,
                "delivery_cost": 50.0,
            },
            {
                "id": 2,
                "name": "Средний короб",
                "weight": 1.5,
                "type_id": 2,
                "content_value": 200,
                "delivery_cost": 75.0,
            },
        ]
    )
    return async_mock


@pytest.fixture
def mock_get_package_query():
    """
    Создает мок-объект для функции get_package_query, возвращающий фиктивные данные посылки.

    :return: AsyncMock с фиктивными данными посылки
    """
    async_mock = AsyncMock(
        return_value={
            "id": 1,
            "name": "Малый короб",
            "weight": 0.5,
            "type_id": 1,
            "content_value": 100,
            "delivery_cost": 50.0,
        }
    )
    return async_mock
