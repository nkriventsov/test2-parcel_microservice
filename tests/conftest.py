import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient

from src.api.v1.endpoints.fx_rate_upd import fx_rate
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
def monkeypatch_fetch_exchange_rate(monkeypatch, mock_fetch_exchange_rate):
    """
    Патчит функцию fetch_exchange_rate, подменяя её на мок-объект для тестирования.

    :param monkeypatch: Фикстура для изменения атрибутов и модулей во время тестов.
    :param mock_fetch_exchange_rate: Мок-объект для функции fetch_exchange_rate.
    """
    monkeypatch.setattr(
        "src.infrastructure.external.currency_service.fetch_exchange_rate",
        mock_fetch_exchange_rate,
    )